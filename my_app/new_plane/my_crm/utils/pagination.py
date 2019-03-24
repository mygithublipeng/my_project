class Pagination:

    def __init__(self, page, all_count, params, per_num=15, max_show=11):
        try:
            page = int(page)
            if page <= 0:
                page = 1
        except Exception as e:
            page = 1
        self.params = params
        self.page = page
        self.all_count = all_count
        self.per_num = per_num
        self.max_show = max_show
        self.page_num, more = divmod(all_count, per_num)
        if more:
            self.page_num += 1
        half_show = max_show // 2
        if self.page_num < max_show:
            self.page_start = 1
            self.page_end = self.page_num
        else:
            if page <= half_show:
                self.page_start = 1
                self.page_end = max_show
            elif page + half_show > self.page_num:
                self.page_start = self.page_num - max_show + 1
                self.page_end = self.page_num
            else:
                self.page_start = page - half_show
                self.page_end = page + half_show

    @property
    def start(self):
        return (self.page - 1) * self.per_num

    @property
    def end(self):
        return self.page * self.per_num

    @property
    def page_html(self):
        li_list = []
        if self.page == 1:
            li_list.append('<li class="disabled" ><a> << </a></li>')
        else:
            self.params['page'] = self.page - 1
            li_list.append('<li ><a href="?{}"> << </a></li>'.format(self.params.urlencode()))

        for i in range(self.page_start, self.page_end + 1):
            self.params['page'] = i
            if self.page == i:
                li_list.append('<li class="active"><a href="?{0}">{1}</a></li>'.format(self.params.urlencode(), i))
            else:
                li_list.append('<li><a href="?{0}">{1}</a></li>'.format(self.params.urlencode(), i))
        self.params['page'] = self.page + 1
        if self.page == self.page_num:
            li_list.append('<li class="disabled" ><a> >> </a></li>')
        else:
            li_list.append('<li ><a href="?{}"> >> </a></li>'.format(self.params.urlencode()))

        return ''.join(li_list)
