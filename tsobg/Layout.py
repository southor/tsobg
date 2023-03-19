
class Layout():

	def removeObject(self, object, recursive=False):
		return self.hasObject(object, recursive=recursive, remove=True)

	# TODO empty methods