-- Ponto focal manual, definido na UI de revisao e usado pelos recortes
-- inteligentes da exportacao. NULL = detectar saliencia automaticamente.
-- Coordenadas relativas (0.0 a 1.0) para sobreviver a qualquer redimensionamento.

ALTER TABLE generations ADD COLUMN focal_x REAL;
ALTER TABLE generations ADD COLUMN focal_y REAL;
