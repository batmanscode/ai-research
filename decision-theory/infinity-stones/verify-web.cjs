#!/usr/bin/env node
/* Compare shipped calculator with separately generated Python evidence. */
'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const M=require('./website/js/model.js');
const record=JSON.parse(fs.readFileSync(path.join(__dirname,'results/verification.json'),'utf8'));
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-10*Math.max(1,Math.abs(b)),`${a} != ${b}`);
const p=record.parameters;
const world=M.worlds(p.lambda,p.beta,p.q,.9);
for(const fixture of [...record.fixtures,record.exponential_fixture]){
  near(world[fixture.name].threshold,fixture.threshold);
  near(world[fixture.name].value,fixture.handover_value);
  near(world[fixture.name].keep,record.keep_value);
}
near(M.bounds(p.lambda,p.beta,1,191,'bounded').low,world.uneven.threshold);
near(M.bounds(p.lambda,p.beta,1,191,'floor').low,record.positive_floor_threshold_infimum);
assert.equal(M.bounds(p.lambda,p.beta,1,191,'mean').low,0);
for(const information of ['bounded','floor','mean']){
  const b=M.bounds(p.lambda,0,1,191,information);
  near(b.low,record.undiscounted_threshold);near(b.high,b.low);
}
for(const [a,b] of [[20,20],[20,191],[1,20]]){
  const result=M.bounds(p.lambda,p.beta,a,b,'bounded');
  near(result.low,result.high);
}
for(const witness of record.mean_only_witnesses){
  near(M.metrics(p.lambda,p.beta,p.q,witness.law).threshold,witness.threshold);
}
let cases=0;
for(const lam of [0,.001,.02,.08])for(const beta of [0,1e-12,.03,.1])
for(const q of [0,.15,.6,1])for(const early of [0,.9,.99]){
  const values=M.worlds(lam,beta,q,early);
  for(const name of ['reliable','exponential','uneven']){
    const r=values[name];
    assert.ok(r.threshold>=0&&r.threshold<=1);
    assert.ok(r.value>=0&&!Number.isNaN(r.value));
    if(Number.isFinite(r.value)&&Number.isFinite(r.keep)&&Math.abs(r.value-r.keep)>1e-7)
      assert.equal(M.preference(q,r.threshold),r.value>r.keep?'handover':'keep');
  }
  near(early+(1-early)*values.slow,20);
  if(beta===0)near(values.reliable.threshold,values.uneven.threshold);
  cases++;
}
assert.equal(M.preference(.2,.2),'tie');
assert.equal(M.metrics(0,0,0,[[20,1]]).value,Infinity);
assert.throws(()=>M.reward(.03,[[20,.9]]),RangeError);
assert.throws(()=>M.worlds(.02,.03,.15,1),RangeError);
assert.throws(()=>M.metrics(.02,.03,-1,[[20,1]]),RangeError);
console.log(`PASS: Python fixture agreement and ${cases} parameter/edge combinations.`);
