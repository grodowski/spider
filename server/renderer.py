# coding: utf8

class Renderer(object):
    def render(s, items):
        ret = ""
        for item in items:
            ret += s.render_item(item)
        return ret

    def render_item(s, item):
        print(item)
        return f"""
        <tr>
            <td>
                <img src="{item.get('img_url')}" />
            </td>
            <td><a href="{item.get('url')}">{item.get('title')}</a></td>
            <td>{item.get('price')}</td>
            <td>{item.get('last_seen')}</td>
        </tr>
        """
