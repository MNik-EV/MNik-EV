import {execFileSync} from 'node:child_process';
import {writeFileSync,mkdirSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {resolve,dirname} from 'node:path';
import {generateSnakeAnimation} from 'generate-snake-animation';

const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const token=process.env.GITHUB_TOKEN || execFileSync('gh',['auth','token'],{encoding:'utf8',stdio:['ignore','pipe','pipe']}).trim();
const palettes={dark:{empty:'#171e26',border:'#2a323b',colors:['#715532','#a47537','#d69743','#ffbb63'],snake:'#82d5e3'},light:{empty:'#ede9e3',border:'#d9d3cb',colors:['#e1c094','#c38b43','#a86524','#814910'],snake:'#147b95'}};
mkdirSync(resolve(root,'assets'),{recursive:true});
const outputs=Object.values(palettes).map(p=>({format:'svg',drawOptions:{colorDots:{1:p.colors[0],2:p.colors[1],3:p.colors[2],4:p.colors[3]},colorEmpty:p.empty,colorDotBorder:p.border,colorSnake:p.snake,sizeCell:16,sizeDot:12,sizeDotBorderRadius:3},animationOptions:{stepDurationMs:100,frameByStep:1}}));
const results=await generateSnakeAnimation({platform:'github',username:'MNik-EV',githubToken:token},outputs);
results.forEach((result,index)=>{
  if(typeof result!=='string'||!result.includes('<svg'))throw Error('Snake generator returned no SVG.');
  const svg=result.replace('</svg>','<style>@media(prefers-reduced-motion:reduce){*{animation:none!important}}</style></svg>');
  writeFileSync(resolve(root,`assets/activity-${index?'light':'dark'}.svg`),svg);
});
writeFileSync(resolve(root,'assets/activity-updated.json'),JSON.stringify({user:'MNik-EV',generatedAt:new Date().toISOString(),source:'GitHub contribution calendar',generator:'Platane/snk 3.5.0'},null,2)+'\n');
console.log('Refreshed the contribution snake in light and dark palettes.');
