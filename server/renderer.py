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
                <img src="{item['img_url']}" />
            </td>
            <td><a href="{item['url']}">{item['title']}</a></td>
            <td>{item['price']}</td>
            <td>{item['last_seen']}</td>
        </tr>
        """
