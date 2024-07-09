class Tracer:
	_instance = None

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(Tracer, cls).__new__(cls, *args, **kwargs)
		return cls._instance

	def __init__(self):
		# Initialize your tracer here (if needed)
		self._bitcounter = 0
		pass

	def T(self, tracestring, bitlength):
		# Implement your tracing logic here
		print(f"@{self._bitcounter:<4}  {tracestring}")
		self._bitcounter += bitlength

tracer = Tracer()