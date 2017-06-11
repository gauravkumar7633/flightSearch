import web

urls = (
  '/booking', 'Index'
)

graph = {'Delhi': ['Vasco de Gama', 'Chennai', 'Kolkatta', 'Mumbai'],
             'Vasco de Gama': ['Delhi', 'Chennai', 'Kolkatta', 'Mumbai'],
             'Chennai': ['Delhi', 'Vasco de Gama', 'Kolkatta', 'Mumbai'],
             'Kolkatta': ['Delhi', 'Chennai', 'Vasco de Gama', 'Mumbai'],
             'Mumbai': ['Delhi', 'Chennai', 'Kolkatta', 'Vasco de Gama']}



app = web.application(urls, globals())

render = web.template.render('templates/')

class Index(object):
    
    def find_all_paths(self, graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if not graph.has_key(start):
            return []
        paths = []
        for node in graph[start]:
            if node not in path:
                newpaths = self.find_all_paths(graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    def compare(self, a, b):
        if(len(a) > len(b)):
            return 1
        else :
            return -1

    def GET(self):
        cities = list(graph.keys())
        return render.hello_form(cities = cities, error='true')

    def getPath(self, start, end):
        return self.find_all_paths(graph, start, end)

    def POST(self):
        form = web.input(source="", destination="")
        source = "%s" % (form.source)
        destination = "%s" % (form.destination)
        cities = list(graph.keys())
        print(source)
        if source == '' or destination == '':
            return render.hello_form(cities = cities, error="Please fill in all the details")
        if source == destination:
            return render.hello_form(cities = cities, error="Source and destination are same. Please enter different Values.")
        

        paths = self.find_all_paths(graph, form.source, form.destination)
        paths.sort(self.compare)
        pathList = []
        for path in paths:
            p = '->'.join(path)
            pathList += [p]

        return render.index(source = source, destination = destination, path = pathList )

if __name__ == "__main__":
    app.run()