<!-- 评论 -->
<template>
<div>
    <div class="ic-comment-list">
        <paginator :page-info='page' :route-name='"forum_topic"' :link-method="'query'" />
        <template v-if="loading">
            <div class="ic-comment" v-for="i in 10" :key="i">
                <avatar :placeholder="true" class="avatar"></avatar>
                <div class="content">
                    <div class="head">
                        <span class="placeholder-text"></span>
                    </div>
                    <div class="post">
                        <span class="placeholder-text"></span>
                        <span class="placeholder-text"></span>
                        <span class="placeholder-text"></span>
                    </div>
                </div>
            </div>
        </template>
        <div v-else-if="page.items.length === 0" class="no-comment">目前尚未有评论</div>
        <div v-else v-for="(i, _) in page.items" :key="i.id" :id="i.id" class="ic-comment">
            <avatar :depth="0" :user="i.user_id" class="avatar"></avatar>
            <div class="content">
                <div class="head">
                    <span>#{{i.post_number || (page.cur_page - 1) * page.info.page_size + _ + 1}}</span>
                    <b><user-link :user="i.user_id" /></b>
                    <span v-if="i.reply_to_cmt_id">
                        <span>回复</span>
                        <b>
                            <a v-if="i.reply_to_cmt_id.user_id" :href="'#' + i.reply_to_cmt_id.id">{{i.reply_to_cmt_id.user_id.nickname}}</a>
                            <span v-else style="color: #999;">已删除内容</span>
                        </b>
                    </span>
                    <span><ic-time :timestamp="i.time" /></span>
                    <a style="float: right" @click="replyTo(i)" href="javascript:void(0)">回复</a>
                </div>
                <blockquote v-if="i.reply_to_cmt_id && i.reply_to_cmt_id.user_id">
                    <div v-html="marked(i.reply_to_cmt_id.content || '')"></div>
                </blockquote>
                <div class="post" v-html="marked(i.content || '')"></div>
            </div>
        </div>
    </div>
    <comment-post @on-commented="commented" :item="item" :post-type="postType" ref="post"></comment-post>
</div>
</template>

<style>
.post > .placeholder-text {
    display: inline-block;
    background-color: #e9e9e9;
    width: 100%;
    height: 16px;
}

/* 注意：评论样式不在 scope 之内，故意为之 */
.ic-comment-list > .no-comment {
    padding: 40px 0;
    text-align: center;
}

.ic-comment {
    display: flex;
    padding: 20px;
    border-bottom: 1px solid #e0e0e0;
}

.ic-comment:target {
    background-color: #ffa;
}

.ic-comment:target > .content {
    background-color: #ffa;
}

.ic-comment:target > .content::after {
   border-color: #ffa;
}

.ic-comment .content > .head {
    font-size: .8em;
    /* padding-bottom: .6em; */
}

.ic-comment .content {
    flex: 1 0 0%;
    padding: 0 10px 0 20px;
}
</style>

<script>
import {marked} from '@/md.js'
import api from '@/netapi.js'
import CommentPost from '../utils/comment-post.vue'

export default {
    props: {
        item: {
            type: Object
        },
        curPage: {
            type: Number,
            default: 1
        },
        withPost: {
            default: false
        },
        postType: {}
    },
    data () {
        return {
            marked,
            loading: true,
            fakeCommentsCount: 1,
            page: { info: {}, items: [] }
        }
    },
    created: async function () {
        // 如果控件加载时即有数据，那么加载数据
        if (this.item.id) {
            this.fetchData()
        }
    },
    mounted: async function () {
    },
    methods: {
        addTest: function () {
            let func = () => {
                this.page.items.push({
                    user_id: {
                        id: 'asdasd',
                        nickname: 'John Doe'
                    }
                })
            }
            $.tpReg('一条评论', func)
        },
        removeTest: function () {
            ;
        },
        commented: function () {
            let info = this.page.info
            let newPage = Math.ceil((info.items_count + 1) / info.page_size)
            this.fetchData(newPage)
        },
        replyTo: function (item) {
            $.scrollTo(document.getElementById('ic-comment-post'))
            document.getElementById('ic-comment-editor').focus()
            this.$refs.post.setReplyTo(item)
        },
        fetchData: async function (thePage) {
            this.loading = true
            thePage = thePage || this.curPage
            this.page.cur_page = thePage

            // 先设置一下伪评论区域，规则非常简单
            if (this.page.s && this.page.s.comment_count) {
                let cc = this.page.s.comment_count
                this.fakeCommentsCount = cc > 20 ? 20 : cc
                if (cc === 0) {
                    this.page = {}
                    this.loading = false
                }
            }

            let ret = await api.comment.list({
                related_id: this.item.id,
                loadfk: {user_id: null, reply_to_cmt_id: {loadfk: {'user_id': null}}}
            }, thePage)
            if (ret.code === api.retcode.SUCCESS) {
                this.page = ret.data
            } else if (ret.code === api.retcode.NOT_FOUND) {
                ;
            } else {
                ;
            }
            this.loading = false
        }
    },
    watch: {
        'item': async function (val) {
            // 如果控件加载时无数据，后续出现数据，那么刷新
            this.fetchData()
        },
        'curPage': async function (val) {
            this.fetchData()
        }
    },
    components: {
        CommentPost
    }
}
</script>
