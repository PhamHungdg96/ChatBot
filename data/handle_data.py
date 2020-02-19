from .crawl_data import get_data
def handle_data(intent):
    intent_map = {
        'ask_death': 'deaths',
        'ask_resolve': 'recovered',
        'ask_confirm': 'confirmed',
        'ask_all': 'all',
        'fallback': 'fallback'
    }
    if intent_map[intent] in ["deaths", "recovered", "confirmed"]:
        return statistic(intent_map[intent])
    if intent_map[intent] == 'all':
        return statistic_all()
    # When fallback
    return "Chatbot chưa xử lý được nội dung bạn nói"
def statistic_all():
    """
    Return all data statistic and generate message to reply
    """
    data = "\n\n".join([statistic(category) for category in ['deaths', 'recovered', 'confirmed']])
    return data


def statistic(category):
    """
    Return all data statistic and generate message to reply
    """
    category_map = {'deaths': 'tử vong', 'recovered': 'đã được chữa khỏi', 'confirmed': 'bị lây nhiễm'}
    data = get_data(category)
    return "Hiện tại đã có {} người {}.\n" \
           "Tại Việt Nam có {} người\n" \
           "Trên toàn cầu có {} người\n" \
           "Cập nhật mới nhất vào {}".format(
        data['latest'],
        category_map[category],
        data['vn_latest'],
        data['global_latest'],
        data['latest_date'])

