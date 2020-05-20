from node.nexus import Nexus
import webbrowser as wb

class Local:
    def __init__(self, nx: Nexus):
        @nx.app.route('/tasks/mozart', methods=['POST'])
        def play_mozart():
            wb.open('https://www.youtube.com/watch?v=sPlhKP0nZII&t=475s')
            return ''
