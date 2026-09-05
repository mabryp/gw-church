// Exercises firestore.rules against the Firestore emulator.
// Run with: npm install && npm test   (needs a Java runtime for the emulator)
import { readFileSync } from 'node:fs';
import { initializeTestEnvironment, assertSucceeds, assertFails } from '@firebase/rules-unit-testing';
import { doc, getDoc, setDoc, deleteDoc, serverTimestamp, Timestamp } from 'firebase/firestore';

const RULES = new URL("../../firestore.rules", import.meta.url);
const env = await initializeTestEnvironment({
  projectId: 'gw-church',
  firestore: { rules: readFileSync(RULES, 'utf8'), host: '127.0.0.1', port: 8080 },
});
await env.clearFirestore();

const THEMES = ['Taco Night', 'Spaghetti', 'Soup & Salad'];

// Same schedule as the page: Sun–Sat (Chicago) votes for NEXT week's Wednesday.
function chicagoParts(d) {
  const f = new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Chicago', year: 'numeric', month: '2-digit', day: '2-digit', weekday: 'short' });
  const p = Object.fromEntries(f.formatToParts(d).map(x => [x.type, x.value]));
  return { y: +p.year, m: +p.month, d: +p.day, wd: p.weekday };
}
function keyOf(wed) { return wed.toISOString().slice(0, 10); }
function wednesdayPlus(days) {
  const { y, m, d, wd } = chicagoParts(new Date());
  const delta = 10 - ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].indexOf(wd);
  return new Date(Date.UTC(y, m - 1, d + delta + days));
}
const KEY = keyOf(wednesdayPlus(0));          // this ballot's Wednesday
const NEXT = keyOf(wednesdayPlus(7));         // the Wednesday after: window not open yet
const PREV = keyOf(wednesdayPlus(-7));        // last ballot: window closed
const NOT_WED = keyOf(wednesdayPlus(1));      // a Thursday
console.log(`ballot key ${KEY} (next ${NEXT}, previous ${PREV})`);
const W = c => `${c}/${KEY}/votes`;
await env.withSecurityRulesDisabled(async ctx => {
  const db = ctx.firestore();
  await setDoc(doc(db, 'polls/defaults'), { themes: THEMES });
  await setDoc(doc(db, 'polls-preview/defaults'), { themes: THEMES });
});
const setWeekDoc = data => env.withSecurityRulesDisabled(async ctx => {
  const ref = doc(ctx.firestore(), `polls/${KEY}`);
  data ? await setDoc(ref, data) : await deleteDoc(ref);
});

const alice = env.authenticatedContext('alice').firestore();
const bob = env.authenticatedContext('bob').firestore();
const anon = env.unauthenticatedContext().firestore();
const vote = (over = {}) => ({ theme: 'Taco Night', at: serverTimestamp(), ...over });
const voter = (over = {}) => ({ name: 'Alice', theme: 'Taco Night', at: serverTimestamp(), ...over });
const V = c => `${c}/${KEY}/voters`;

let pass = 0, fail = 0;
async function t(name, expectOk, p) {
  try {
    await (expectOk ? assertSucceeds(p) : assertFails(p));
    pass++; console.log(`  ok   ${name}`);
  } catch (e) {
    fail++; console.log(`  FAIL ${name}\n       ${String(e.message || e).split('\n')[0]}`);
  }
}

console.log('allow paths');
await t('create own vote', true, setDoc(doc(alice, `${W('polls')}/alice`), vote()));
await t('update own vote (change theme)', true, setDoc(doc(alice, `${W('polls')}/alice`), vote({ theme: 'Spaghetti' })));
await t('second voter', true, setDoc(doc(bob, `${W('polls')}/bob`), vote()));
await t('vote in polls-preview', true, setDoc(doc(alice, `${W('polls-preview')}/alice`), vote()));
await t('voter record with name', true, setDoc(doc(alice, `${V('polls')}/alice`), voter()));
await t('voter record updated', true, setDoc(doc(alice, `${V('polls')}/alice`), voter({ theme: 'Spaghetti' })));
await t('voter name at 60 chars', true, setDoc(doc(bob, `${V('polls')}/bob`), voter({ name: 'B'.repeat(60) })));
await t('anon reads defaults', true, getDoc(doc(anon, 'polls/defaults')));
await t('anon reads a vote', true, getDoc(doc(anon, `${W('polls')}/alice`)));
await t('anon reads preview vote', true, getDoc(doc(anon, `${W('polls-preview')}/alice`)));

console.log('per-Wednesday override doc');
await setWeekDoc({ themes: ['Chili'], closesAt: Timestamp.fromDate(new Date('2099-01-01T00:00:00Z')) });
await t('override theme accepted', true, setDoc(doc(alice, `${W('polls')}/alice`), vote({ theme: 'Chili' })));
await t('defaults theme rejected when the week overrides the list', false, setDoc(doc(alice, `${W('polls')}/alice`), vote({ theme: 'Taco Night' })));
await setWeekDoc({ themes: ['Chili'], closesAt: Timestamp.fromDate(new Date('2020-01-01T00:00:00Z')) });
await t('vote after an early closesAt', false, setDoc(doc(alice, `${W('polls')}/alice`), vote({ theme: 'Chili' })));
await setWeekDoc(null);

console.log('voting window');
await t('vote for the Wednesday after next (window not open)', false, setDoc(doc(alice, `polls/${NEXT}/votes/alice`), vote()));
await t('vote for last ballot\'s Wednesday (window closed)', false, setDoc(doc(alice, `polls/${PREV}/votes/alice`), vote()));
await t('key that is not a Wednesday', false, setDoc(doc(alice, `polls/${NOT_WED}/votes/alice`), vote()));
await t('malformed key', false, setDoc(doc(alice, 'polls/2026-W37/votes/alice'), vote()));
await t('impossible date', false, setDoc(doc(alice, 'polls/2026-13-45/votes/alice'), vote()));

console.log('deny paths');
await t('unauthenticated write', false, setDoc(doc(anon, `${W('polls')}/anon`), vote()));
await t('write under someone else\'s uid', false, setDoc(doc(alice, `${W('polls')}/bob`), vote()));
await t('theme not in list', false, setDoc(doc(alice, `${W('polls')}/alice`), vote({ theme: 'Sushi' })));
await t('theme not a string', false, setDoc(doc(alice, `${W('polls')}/alice`), vote({ theme: 3 })));
await t('name on the public vote doc', false, setDoc(doc(alice, `${W('polls')}/alice`), vote({ name: 'Alice' })));
await t('missing theme', false, setDoc(doc(alice, `${W('polls')}/alice`), { at: serverTimestamp() }));
await t('voter: read own record', false, getDoc(doc(alice, `${V('polls')}/alice`)));
await t('voter: anon read', false, getDoc(doc(anon, `${V('polls')}/alice`)));
await t('voter: empty name', false, setDoc(doc(alice, `${V('polls')}/alice`), voter({ name: '' })));
await t('voter: name at 61 chars', false, setDoc(doc(alice, `${V('polls')}/alice`), voter({ name: 'A'.repeat(61) })));
await t('voter: missing name', false, setDoc(doc(alice, `${V('polls')}/alice`), vote()));
await t('voter: theme not in list', false, setDoc(doc(alice, `${V('polls')}/alice`), voter({ theme: 'Sushi' })));
await t('voter: someone else\'s uid', false, setDoc(doc(alice, `${V('polls')}/bob`), voter()));
await t('voter: unauthenticated', false, setDoc(doc(anon, `${V('polls')}/anon`), voter()));
await t('voter: delete', false, deleteDoc(doc(alice, `${V('polls')}/alice`)));
await t('voter: window closed', false, setDoc(doc(alice, `polls/${PREV}/voters/alice`), voter()));
await t('extra field', false, setDoc(doc(alice, `${W('polls')}/alice`), vote({ extra: true })));
await t('client-supplied timestamp', false, setDoc(doc(alice, `${W('polls')}/alice`), vote({ at: Timestamp.now() })));
await t('delete own vote', false, deleteDoc(doc(alice, `${W('polls')}/alice`)));
await t('vote under the defaults doc', false, setDoc(doc(alice, 'polls/defaults/votes/alice'), vote()));
await t('write a config doc', false, setDoc(doc(alice, `polls/${KEY}`), { themes: ['Cake'] }));
await t('write defaults', false, setDoc(doc(alice, 'polls/defaults'), { themes: ['Cake'] }));
await t('unrelated collection write', false, setDoc(doc(alice, `foo/${KEY}/votes/alice`), vote()));
await t('unrelated collection read', false, getDoc(doc(anon, 'foo/bar')));
await env.withSecurityRulesDisabled(async ctx => { await deleteDoc(doc(ctx.firestore(), 'polls-preview/defaults')); });
await t('collection whose defaults doc is missing', false, setDoc(doc(alice, `${W('polls-preview')}/alice`), vote()));

await env.cleanup();
console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
