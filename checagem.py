from envia import send

def check(entrada1,entrada2,entrada3,entrada4): # verifica se tem todas as variáveis necessárias para calcular os pontos
    if(entrada1 != -99 and entrada2 != -99 and entrada3 != -99 and entrada4 != -99): 

      send(entrada1,entrada2,entrada3,entrada4)
      print("\n Foi checado \n")
      entrada1 = -99
      entrada2 = -99
      entrada3 = -99
      entrada4 = -99