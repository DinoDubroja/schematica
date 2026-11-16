"""Isolated hosted Review checks, including actual subscription-backed image inspection.

Requires the browser checks' image comments. Never targets production; never publishes.
"""
from support import APP
import argparse
import copy
import hashlib
import json
from pathlib import Path
import time
import urllib.error
import urllib.parse
import urllib.request
from review_client import Client,write_json
from review_desktop import Connector
from verify_review_hosted import BrowserSession,rejected


def run(config_path,fixtures_path,output,resume=False):
    config=json.loads(Path(config_path).read_text());assert urllib.parse.urlparse(config['url']).hostname.startswith('schematica-review-validation.'),'Validation service only'
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    fixtures=json.loads(Path(fixtures_path).read_text());client=Client(config);user=BrowserSession(config);other=BrowserSession(config);checks=[]
    before=json.loads((output/'before.json').read_text()) if resume else client.state()
    if not resume:write_json(output/'before.json',before)
    catalog_before=client.request('/library/catalog.json',authenticated=False)
    ids={key:value['symbol'] for key,value in fixtures.items()}
    active=[s['id'] for s in before['symbols'].values() if s.get('candidate') and not s.get('discarded')]
    assert all(s.startswith(('test-','review-ui-')) for s in active),'Unexpected real candidate on validation service'
    # Scope global Process Review to these fixtures without deleting older evidence.
    if not resume:user.action('discard',{'symbols':active});user.action('restore',{'symbols':[ids['question']]})
    question_revision=client.state()['symbols'][ids['question']]['latest']
    question_text='Make the top bar shorter, and do not change the length of any bar. These two requirements are equally mandatory; ask which one should apply.'
    if not any(c['text']==question_text and any(t['symbol']==ids['question'] and t['revision']==question_revision for t in c['targets']) for c in client.state()['comments'].values()):
        user.action('comment',{'text':question_text,'targets':[{'symbol':ids['question'],'revision':question_revision}]})
    question_job=next(j['id'] for j in client.state()['jobs'].values() if j['status']=='Needs your answer' and any(t['symbol']==ids['question'] for t in j['corrections'])) if resume else user.action('process',{})['id']
    if not resume:user.action('restore',{'symbols':[ids['image-a'],ids['image-b'],ids['stale'],ids['failure']]})
    for key in ([] if resume else ['stale','failure']):
        s=client.state()['symbols'][ids[key]]
        user.action('comment',{'text':'Synthetic request: shorten only the top bar.','targets':[{'symbol':s['id'],'revision':s['latest']}]})
    if not resume:
        queued=user.action('process',{});count=len(client.state()['jobs'])
        duplicate=user.action('process',{});assert not duplicate['ids'] and len(client.state()['jobs'])==count
    checks.append('Repeated Process Review does not duplicate a queued correction')
    stale_revision=client.state()['symbols'][ids['stale']]['latest']
    if not resume:user.action('comment',{'text':'Later feedback: leave the top bar unchanged.','targets':[{'symbol':ids['stale'],'revision':stale_revision}]})
    # Every image is private, checksum verified and accessible in a second session.
    comments=[c for c in client.state()['comments'].values() if any(t['symbol']==ids['image-a'] and t['revision']==fixtures['image-a']['revision'] for t in c['targets'])]
    assert any(c.get('attachments') for c in comments),'Run the browser image-comment check first'
    image=next(a for c in comments for a in c.get('attachments',[]))
    raw=other.request('/review/images/'+image['hash']);assert hashlib.sha256(raw).hexdigest()==image['hash']
    rejected(lambda:urllib.request.urlopen(urllib.request.Request(config['url']+'/review/images/'+image['hash'],headers={'User-Agent':'SchematicaReviewValidation/1.0'})),401)
    rejected(lambda:user.request('/api/review/images',{'hash':'a'*64,'mime':'image/svg+xml','body':'PHN2Zy8+'}),413)
    missing={'hash':'b'*64,'mime':'image/png','bytes':100,'name':'missing.png'}
    rejected(lambda:user.action('comment',{'text':'Missing image','targets':[{'symbol':ids['image-a'],'revision':fixtures['image-a']['revision']}],'attachments':[missing]}),400)
    checks.append('Images require authentication and complete validated uploads before comment save')
    connector=Connector(config_path)
    # Use the actual image-aware Codex path. Calls return bounded JSON/TeX only.
    for _ in range(30):
        claim=client.action('claim',{'protocol':2})['job']
        if not claim:
            if any(j['status']=='Working' and any(t['symbol'] in ids.values() for t in j['corrections']) for j in client.state()['jobs'].values()):time.sleep(8);continue
            break
        target=(claim['corrections'] or claim['publications'])[0]
        assert not claim['publications'],'This check must never publish a fixture'
        assert target['symbol'] in [ids[k] for k in ['question','image-a','image-b','stale','failure']]
        if target['symbol']==ids['failure']:
            client.action('fail',{'job':claim['id'],'lease':claim['lease'],'error':'Synthetic transient failure; safe to retry.'});continue
        if target['symbol']==ids['stale']:raise AssertionError('Changed feedback should have been skipped as stale')
        print('Processing isolated fixture:',target['symbol'],flush=True)
        connector.job=claim;connector.lost_lease=False
        import threading
        renewal=threading.Thread(target=connector.renew_loop,daemon=True);renewal.start()
        try:connector.process(claim)
        finally:connector.stop.set();renewal.join(timeout=5);connector.stop.clear();connector.job=None
        saved=client.state()['jobs'][claim['id']]
        if target['symbol']==ids['question']:
            assert saved['status']=='Needs your answer' and saved['question']['text']
            checks.append('Actual agent asks one focused question for conflicting feedback')
        else:
            assert saved['status']=='Ready to review' and saved['results']
            result=saved['results'][0];symbol=client.state()['symbols'][target['symbol']]
            assert symbol['latest']==result['revision'] and symbol['selected']!=result['revision'] and symbol.get('published')!=result['revision']
            revision=client.revision(result['revision']);assert revision['parent']==target['revision'] and len(revision['symbol']['configurations'])==18
            assert revision['change']['why'] and revision['change']['feedback']
            checks.append('Direct correction returned 18 configurations, a summary and a new Unverified revision: '+target['symbol'])
            if target['symbol']==ids['image-a']:
                interpretation=Path(config['work'])/'jobs'/claim['id'].replace(':','-')/(target['symbol']+'-'+target['signature'][:16])/'interpretation/answer.json'
                observed=json.loads(interpretation.read_text());assert '47' in json.dumps(observed['image_observations']),observed['image_observations']
                write_json(output/'image-inspection.json',observed)
                checks.append('Actual agent inspected the private image and identified the number visible only in its pixels')
    final=client.state();assert final['jobs'][question_job]['status']=='Needs your answer'
    assert all(any(r['symbol']==ids[key] for j in final['jobs'].values() for r in j.get('results',[])) for key in ['image-a','image-b'])
    checks.append('A blocked correction did not stop two independent real corrections')
    for key in ['image-a','image-b']:
        s=final['symbols'][ids[key]];r=client.revision(s['latest']);assert r['parent']==fixtures[key]['revision'] and len(r['symbol']['configurations'])==18 and s['selected']!=r['id'] and s.get('published')!=r['id']
    observed=json.loads((output/'image-inspection.json').read_text());assert '47' in json.dumps(observed['image_observations'])
    checks.append('Both saved corrections remain Unverified, with 18 configurations each; real image inspection retained')
    assert any(j['status']=='Stale' for j in final['jobs'].values() if any(t['symbol']==ids['stale'] for t in j['corrections']))
    assert any(j['status']=='Failed' for j in final['jobs'].values() if any(t['symbol']==ids['failure'] for t in j['corrections']))
    checks.append('Changed feedback becomes stale; independent failure remains retryable')
    assert client.request('/library/catalog.json',authenticated=False)==catalog_before
    assert all(final['symbols'][sid].get('published')==s.get('published') for sid,s in before['symbols'].items())
    checks.append('Validation public catalog unchanged; zero test publications')
    write_json(output/'results.json',{'passed':len(checks),'checks':checks,'question_job':question_job,'fixtures':fixtures,'production_writes':0,'publications':0})
    write_json(output/'after.json',final)
    print(json.dumps({'passed':len(checks),'publications':0,'production_writes':0}),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--config',required=True);p.add_argument('--fixtures',required=True);p.add_argument('--output',required=True);p.add_argument('--resume',action='store_true');a=p.parse_args();run(a.config,a.fixtures,a.output,a.resume)
