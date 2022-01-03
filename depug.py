from Detection import LineDetector

ld = LineDetector()
points = [(940, 578), (936, 512), (931, 426), (924, 362),
          (928, 305), (925, 240), (921, 208)]
print(ld.fit(points))
