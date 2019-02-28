from serialize import comptePointsMatching

print comptePointsMatching('vigicrues','V712401501-q',lambda v: v>3.0 and v<60.0)/3600*24
print comptePointsMatching('vigicrues','Y561501001-q',lambda v: v>3.0 and v<60.0)
 
