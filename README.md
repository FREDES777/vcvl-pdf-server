# vcvl-pdf-server

## Compensação de início do lote

Os scripts de impressão física da Lotofácil, Lotofácil da Independência, Mega-Sena, Quina e Quina de São João aceitam `offsetLoteMm` no payload. O valor representa a diferença em milímetros em relação à medida de referência do lote atual: positivo desloca as marcações para baixo e negativo para cima. Se omitido, o padrão é `0` e as calibrações existentes permanecem inalteradas.