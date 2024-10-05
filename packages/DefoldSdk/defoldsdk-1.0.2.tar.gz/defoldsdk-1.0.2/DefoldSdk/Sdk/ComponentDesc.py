
from .naitivesdk import nsdk

class ComponentDesc(nsdk.ComponentDesc) : 
	__mule__ = True
	def __preinit__(self,*args,**kwargs) : 
		self.component = ""