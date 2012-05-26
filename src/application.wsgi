import web

urls = (
    '/(.*)', 'hello'
)

class hello:
    def GET(self, name):
        if not name:
            name = 'World'
        return 'Huhu, %s!' % (name)

if __name__ == "__main__":
    app.run()

app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()
