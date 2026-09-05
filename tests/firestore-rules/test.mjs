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
await env.withSecurityRulesDisabled(async ctx => {
  const db = ctx.firestore();
  await setDoc(doc(db, 'polls/defaults'), { themes: THEMES });
  await setDoc(doc(db, 'polls-preview/defaults'), { themes: THEMES });
  // per-week override, already closed
  await setDoc(doc(db, 'polls/2026-W30'), { themes: ['Chili'], closesAt: Timestamp.fromDate(new Date('2026-07-21T23:00:00Z')) });
  // per-week override, still open
  await setDoc(doc(db, 'polls/2026-W40'), { themes: ['Chili'], closesAt: Timestamp.fromDate(new Date('2099-01-01T00:00:00Z')) });
  // a collection with no defaults doc at all
  await setDoc(doc(db, 'polls-preview/2026-W50/votes/seed'), { name: 'x', theme: 'Taco Night', at: Timestamp.now() });
});

const alice = env.authenticatedContext('alice').firestore();
const bob = env.authenticatedContext('bob').firestore();
const anon = env.unauthenticatedContext().firestore();
const vote = (over = {}) => ({ name: 'Alice', theme: 'Taco Night', at: serverTimestamp(), ...over });

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
await t('create own vote', true, setDoc(doc(alice, 'polls/2026-W37/votes/alice'), vote()));
await t('update own vote (change theme)', true, setDoc(doc(alice, 'polls/2026-W37/votes/alice'), vote({ theme: 'Spaghetti' })));
await t('second voter', true, setDoc(doc(bob, 'polls/2026-W37/votes/bob'), vote({ name: 'Bob' })));
await t('vote in polls-preview', true, setDoc(doc(alice, 'polls-preview/2026-W37/votes/alice'), vote()));
await t('vote in open per-week override with its theme', true, setDoc(doc(alice, 'polls/2026-W40/votes/alice'), vote({ theme: 'Chili' })));
await t('name at 60 chars', true, setDoc(doc(bob, 'polls/2026-W37/votes/bob'), vote({ name: 'B'.repeat(60) })));
await t('anon reads defaults', true, getDoc(doc(anon, 'polls/defaults')));
await t('anon reads a vote', true, getDoc(doc(anon, 'polls/2026-W37/votes/alice')));
await t('anon reads preview vote', true, getDoc(doc(anon, 'polls-preview/2026-W37/votes/alice')));

console.log('deny paths');
await t('unauthenticated write', false, setDoc(doc(anon, 'polls/2026-W37/votes/anon'), vote()));
await t('write under someone else\'s uid', false, setDoc(doc(alice, 'polls/2026-W37/votes/bob'), vote()));
await t('theme not in list', false, setDoc(doc(alice, 'polls/2026-W37/votes/alice'), vote({ theme: 'Sushi' })));
await t('theme not a string', false, setDoc(doc(alice, 'polls/2026-W37/votes/alice'), vote({ theme: 3 })));
await t('empty name', false, setDoc(doc(alice, 'polls/2026-W37/votes/alice'), vote({ name: '' })));
await t('name at 61 chars', false, setDoc(doc(alice, 'polls/2026-W37/votes/alice'), vote({ name: 'A'.repeat(61) })));
await t('missing name', false, setDoc(doc(alice, 'polls/2026-W37/votes/alice'), { theme: 'Taco Night', at: serverTimestamp() }));
await t('extra field', false, setDoc(doc(alice, 'polls/2026-W37/votes/alice'), vote({ extra: true })));
await t('client-supplied timestamp', false, setDoc(doc(alice, 'polls/2026-W37/votes/alice'), vote({ at: Timestamp.now() })));
await t('delete own vote', false, deleteDoc(doc(alice, 'polls/2026-W37/votes/alice')));
await t('vote after closesAt', false, setDoc(doc(alice, 'polls/2026-W30/votes/alice'), vote({ theme: 'Chili' })));
await t('defaults theme in a week that overrides the list', false, setDoc(doc(alice, 'polls/2026-W40/votes/alice'), vote({ theme: 'Taco Night' })));
await t('bad week id', false, setDoc(doc(alice, 'polls/junk/votes/alice'), vote()));
await t('vote under the defaults doc', false, setDoc(doc(alice, 'polls/defaults/votes/alice'), vote()));
await t('write a config doc', false, setDoc(doc(alice, 'polls/2026-W37'), { themes: ['Cake'] }));
await t('write defaults', false, setDoc(doc(alice, 'polls/defaults'), { themes: ['Cake'] }));
await t('unrelated collection write', false, setDoc(doc(alice, 'foo/2026-W37/votes/alice'), vote()));
await t('unrelated collection read', false, getDoc(doc(anon, 'foo/bar')));
await env.withSecurityRulesDisabled(async ctx => { await deleteDoc(doc(ctx.firestore(), 'polls-preview/defaults')); });
await t('collection whose defaults doc is missing', false, setDoc(doc(alice, 'polls-preview/2026-W50/votes/alice'), vote()));

await env.cleanup();
console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
