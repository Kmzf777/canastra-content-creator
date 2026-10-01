// Registra o gancho de resolucao de `.ts` e liga o type stripping do Node.
//
// Usado como `node --import ./scripts/_registrar-ts.mjs <script>.mjs`. Existe para que
// a linha de comando nao tenha que repetir `--experimental-strip-types` mais um
// `register(...)` em todo script que importa `src/`.
//
// Ver `scripts/_resolver-ts.mjs` para por que o gancho e necessario: o tsconfig usa
// `moduleResolution: "bundler"`, o codigo de `src/` importa sem extensao, e o
// resolvedor ESM cru do Node devolve ERR_MODULE_NOT_FOUND.

import {register} from 'node:module';

register('./_resolver-ts.mjs', import.meta.url);
