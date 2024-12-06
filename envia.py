from SimCell import celula
from SimCell2 import celula_1
def send(entrada1, entrada2, entrada3, entrada4): 
    
  global V, Pplot, Iplot, Pplot2, Iplot2
  print("chegou em send")
  celula(entrada1, entrada2, entrada3, entrada4)
  
  celula_1(entrada1, entrada2, entrada3, entrada4)