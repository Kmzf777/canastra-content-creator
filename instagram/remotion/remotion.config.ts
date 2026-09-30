// Config de render do motor de video Canastra.
// Ver https://www.remotion.dev/docs/config
import {Config} from '@remotion/cli/config';

// H.264 em MP4: e o que Instagram e Mercado Livre aceitam sem reencode agressivo.
Config.setVideoImageFormat('jpeg');
Config.setCodec('h264');

// Overwrite ligado: o pipeline reescreve a mesma saida a cada rodada de conferencia.
Config.setOverwriteOutput(true);
