/* The research model only: shared by the browser and its Node fixture audit. */
(function(root){
  'use strict';
  function validate(lam,beta,q){
    if(![lam,beta,q].every(Number.isFinite)||lam<0||beta<0||q<0||q>1)throw new RangeError('Invalid model parameters');
  }
  function reward(beta,law){
    if(!Number.isFinite(beta)||beta<0||!law.length)throw new RangeError('Invalid pause law');
    let sum=0,total=0;
    for(const [time,p] of law){
      if(!Number.isFinite(time)||time<=0||!Number.isFinite(p)||p<0)throw new RangeError('Pause times must be positive');
      total+=p;sum+=p*(beta===0?time:-Math.expm1(-beta*time)/beta);
    }
    if(Math.abs(total-1)>1e-10)throw new RangeError('Probabilities must sum to one');
    return sum;
  }
  function fromReward(lam,beta,q,h){
    validate(lam,beta,q);
    const denominator=q+(1-q)*beta*h;
    return {threshold:lam*h/(1+lam*h),value:denominator===0?Infinity:(1-q)*h/denominator,
      keep:lam+beta===0?Infinity:1/(lam+beta)};
  }
  function metrics(lam,beta,q,law){return fromReward(lam,beta,q,reward(beta,law));}
  function worlds(lam,beta,q,early){
    if(!Number.isFinite(early)||early<0||early>=1)throw new RangeError('Early-return chance must be below one');
    const slow=(20-early)/(1-early);
    return {reliable:metrics(lam,beta,q,[[20,1]]),
      exponential:fromReward(lam,beta,q,1/(beta+1/20)),
      uneven:metrics(lam,beta,q,[[1,early],[slow,1-early]]),slow};
  }
  function bounds(lam,beta,a,b,information){
    validate(lam,beta,0);
    if(!['bounded','floor','mean'].includes(information))throw new RangeError('Unknown information case');
    if(!Number.isFinite(a)||!Number.isFinite(b)||a<=0||a>20||b<20)throw new RangeError('Bounds must contain the mean');
    const high=metrics(lam,beta,0,[[20,1]]).threshold;
    if(beta===0)return {low:high,high,attained:true};
    if(information==='mean')return {low:0,high,attained:lam===0};
    if(a===20)return {low:high,high,attained:true};
    if(information==='floor')return {low:metrics(lam,beta,0,[[a,1]]).threshold,high,attained:lam===0};
    if(b===20)return {low:high,high,attained:true};
    return {low:metrics(lam,beta,0,[[a,(b-20)/(b-a)],[b,(20-a)/(b-a)]]).threshold,high,attained:true};
  }
  function preference(q,threshold){return Math.abs(q-threshold)<1e-10?'tie':q<threshold?'handover':'keep';}
  const api={reward,fromReward,metrics,worlds,bounds,preference};
  if(typeof module==='object'&&module.exports)module.exports=api;else root.StonesModel=api;
})(typeof window==='undefined'?this:window);
