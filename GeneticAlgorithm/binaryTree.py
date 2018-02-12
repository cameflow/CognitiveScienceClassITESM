# Clase Nodo
# Tiene dos hijos y un valor
class TreeNode:
	def __init__(self,value):
		self.left = None
		self.right = None
		self.data = value

# Clase árbol binario
# Tiene una raiz y esa raiz es de tipo Nodo
class Tree:

	def __init__(self):
		self.root = None

	# Agregar un nodos checa primero si el árbol está vacío y si lo está agrega ese valor como su raiz.
	# Checa si lo que se está agregando es un signo para convertirlo en la nueva raiz.
	def addNode(self, value):
		if (self.root == None):
			self.root = TreeNode(value)

		signs = ['+','-','*','/','^']

		if value in signs:
			aux = self.root
			self.root = TreeNode(value)
			self.root.left = aux
		else:
			self.root.right = TreeNode(value)


	def printTree(self,node):
		if (node.left == None):
			return node.data
		else:
			str = "("
			str += self.printTree(node.left)
			str += node.data
			str += self.printTree(node.right)
			str += ")"
			return str





