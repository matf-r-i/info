\ Model Electro-Poly
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  50 number-model-1-in-house + 83 number-model-2-in-house
   + 130 number-model-3-in-house + 61 number-model-1-by-from-competitor
   + 97 number-model-2-by-from-competitor
   + 145 number-model-3-by-from-competitor
Subject To
 resource-wiring: 2 number-model-1-in-house + 1.5 number-model-2-in-house
   + 3 number-model-3-in-house <= 10000
 resources-harnessing: number-model-1-in-house + 2 number-model-2-in-house
   + number-model-3-in-house <= 5000
 demand-model-1: number-model-1-in-house
   + number-model-1-by-from-competitor = 3000
 demand-model-2: number-model-2-in-house
   + number-model-2-by-from-competitor = 2000
 demand-model-3: number-model-3-in-house
   + number-model-3-by-from-competitor = 900
Bounds
End
