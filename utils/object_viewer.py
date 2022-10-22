class ObjectParser(object):
    def __init__(self, obj, endpoint=False):
        self.obj = obj
        self.mode = endpoint
        self.structure = []
        self.structure_endpoint = []
        self.path = []
        self.mode_obj = self.structure_endpoint if self.mode else self.structure_endpoint
        self.parse_object(obj)

    def parse_object(self, obj):
        print(self.path)
        if isinstance(obj, dict):
            for i in obj.keys():
                self.path.append(f"['{i}']")
                self.structure.append( tuple(self.path) )
                self.parse_object(obj[i])
                self.path.pop(-1)
        elif isinstance(i, int) or isinstance(i, float) or isinstance(i, str):
            self.structure_endpoint.append(f"{''.join(self.path)}: {i}")

        elif isinstance(obj, list):
            for idx, i in enumerate(obj):
                print(self.path)
                if isinstance(i, int) or isinstance(i, float) or isinstance(i, str):
                    self.structure_endpoint.append(f"{''.join(self.path)}: {i}")
#                self.path.append(f"[0]")
                self.path.append(f"[{idx}]")
                self.structure.append( tuple(self.path) )
                self.parse_object(i)
                self.path.pop(-1)

# permet de recréer la structure brut du json
# permet d'afficher 1 endpoint par ligne et de print la valeur associée
# is_container()
# is_endpoint()
    def __iter__(self):
        self.n = 0
        self.max = len(self.mode_obj)
        return self

    def __next__(self):
        if self.mode:
            if self.n < self.max:
                return self.structure_endpoint[self.n]
        else:
            if self.n < self.max:
                key = "".join(self.structure[self.n])
                key = self.structure[self.n]
                self.n += 1
#            value = eval(f"{self.obj}{key}")
#            if isinstance(value, int) or isinstance(value, float) or isinstance(value, str):
#                return f"{key}: {value}"
#            return f"{key}"
            return key
        raise StopIteration

    def __str__(self):
        if self.mode:
            return "\n".join( [ i for i in self.structure_endpoint ] )
        return "\n".join( [ "".join(i) for i in self.structure ] )

    def log(self):
        return "\n".join( [ "".join(i) for i in self.structure ] )
