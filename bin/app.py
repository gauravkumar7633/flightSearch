import web

urls = (
  '/hello', 'Index'
)

app = web.application(urls, globals())

render = web.template.render('templates/')

class Index(object):
    graph = {'delhi': ['panji', 'chennai', 'kolkatta', 'mumbai'],
             'panji': ['delhi', 'chennai', 'kolkatta', 'mumbai'],
             'chennai': ['delhi', 'panji', 'kolkatta', 'mumbai'],
             'kolkatta': ['delhi', 'chennai', 'panji', 'mumbai'],
             'mumbai': ['delhi', 'chennai', 'kolkatta', 'panji']}

    def find_all_paths(self, graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if not graph.has_key(start):
            return []
        paths = []
        for node in graph[start]:
            if node not in path:
                newpaths = self.find_all_paths(self.graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    def compare(self, a, b):
        if(len(a) > len(b)):
            return 1
        else :
            return -1

    def GET(self):
        return render.hello_form()

    def getPath(self, start, end):
        return self.find_all_paths(self.graph, start, end)

    def POST(self):
        form = web.input(name="Nobody", greet="Hello")
        source = "%s" % (form.source)
        destination = "%s" % (form.destination)

        paths = self.find_all_paths(self.graph, form.source, form.destination)
        paths.sort(self.compare)
        print(paths)
        pathList = '\n'
        for path in paths:
            p = '->'.join(path)
            pathList += p
            pathList += '\n'

        path1 = '->'.join(path)
        return render.index(source = source, destination = destination, path = pathList )

if __name__ == "__main__":
    app.run()