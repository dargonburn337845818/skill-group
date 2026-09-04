// Oracle reference solution: poem only, passes the verifier.
import fs from 'node:fs';
fs.writeFileSync('poem.txt', '春水初生绿，东风入旧枝。\n花开人独立，燕子正归时。\n');
fs.writeFileSync('output.txt', '春水初生绿，东风入旧枝。\n花开人独立，燕子正归时。\n');
