l_bow.velo(50)
d = {"proby": 0, "zera": 0, "jeden":0, "dwa": 0, "trzy": 0, "wiecej": 0, "razem": 0}
starta = time.ticks_ms()
def foo(dly=0.4):
  start = time.ticks_ms()
  l_bow.prog()
  time.sleep(dly)
  c=len(l_cam.get())
  print("Znaleziono: %s"%c)
  d["proby"]=d["proby"]+1
  if c == 0:
    d["zera"]=d["zera"]+1
  elif c == 1:
    d["jeden"]=d["jeden"]+1
    d["razem"]=d["razem"]+c
  elif c == 2:
    d["dwa"]=d["dwa"]+1
    d["razem"]=d["razem"]+c
  elif c == 3:
    d["trzy"]=d["trzy"]+1
    d["razem"]=d["razem"]+c
  else:
    d["wiecej"]=d["wiecej"]+1
    d["razem"]=d["razem"]+c
  d["czas"]=time.ticks_diff(time.ticks_ms(), start)
  d["czas_testu"]=time.ticks_diff(time.ticks_ms(), starta)
  print(d)
for x in range(10):
  foo()

#main_binary.py
{'proby': 100, 'razem': 127, 'czas_testu': 153614, 'trzy': 12, 'wiecej': 4, 'jeden': 28, 'dwa': 23, 'czas': 1518, 'zera': 33}
#main_triangles.py 20pcs
{'proby': 100, 'razem': 149, 'czas_testu': 132611, 'trzy': 10, 'wiecej': 9, 'jeden': 35, 'dwa': 23, 'czas': 1178, 'zera': 23}
{'proby': 100, 'razem': 128, 'czas_testu': 132186, 'trzy': 4, 'wiecej': 2, 'jeden': 34, 'dwa': 37, 'czas': 1644, 'zera': 23}
#main_triangles.py 30pcs
{'proby': 100, 'razem': 212, 'czas_testu': 134109, 'trzy': 19, 'wiecej': 18, 'jeden': 23, 'dwa': 24, 'czas': 1692, 'zera': 16}
#main_triangles.py 40pcs
{'proby': 100, 'razem': 252, 'czas_testu': 135517, 'trzy': 22, 'wiecej': 21, 'jeden': 24, 'dwa': 29, 'czas': 1182, 'zera': 4}
#main_triangles.py 50pcs
{'proby': 100, 'razem': 275, 'czas_testu': 135353, 'trzy': 29, 'wiecej': 28, 'jeden': 18, 'dwa': 20, 'czas': 1162, 'zera': 5}
#main_triangles.py 60pcs
{'proby': 100, 'razem': 233, 'czas_testu': 135865, 'trzy': 16, 'wiecej': 24, 'jeden': 29, 'dwa': 24, 'czas': 1680, 'zera': 7}
{'proby': 100, 'razem': 205, 'czas_testu': 134597, 'trzy': 21, 'wiecej': 11, 'jeden': 19, 'dwa': 35, 'czas': 1680, 'zera': 14}
#MemoryError: memory allocation failed, allocating 1416782180 bytes
