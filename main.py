import praw
import json
from praw.models import MoreComments
import pprint
import csv
import codecs
def main():
    r= praw.Reddit('bot1')

    output_file= open('output.csv','wb')
    output_writer=csv.writer(output_file)
    
    i = 0

    filecount = 1
    fw1 = open("/home/farig/Downloads/reddit2/postInfo.txt", "w")
    fw1.write("postCounter\tpostId\tposter\ttitle\ttime\tups\tdowns\n")
    fw = open("/home/farig/Downloads/reddit2/post contents/file" + str(filecount) + ".txt", "w")
    postcount = 0
    
    for submission in r.subreddit('depression').top(limit=10):
        i = i + 1
	if i == 1 or i == 2: continue
        print (submission.url)


        postDic = {}
        postID = submission.id
        if hasattr(submission, 'author'):
            if submission.author != None:
                postAuthor = str(submission.author)
            else:
                postAuthor = ''
        else:
            postAuthor = ''

        postText = str(submission.selftext.encode('utf8'))
	fw.write(postText + "\n")
	fw.write("--------------------" + "\n")
        postcount = postcount + 1
	if postcount == 500:
	    postcount = 0
	    fw.close()
	    filecount = filecount + 1
	    fw = open("/home/farig/Downloads/reddit2/post contents/file" + str(filecount) + ".txt", "w")
        postSubreddit = str(submission.subreddit)
        postTitle = str(submission.title.encode('utf8'))
        postUrl = submission.url
        postUps = submission.ups
        postDown = submission.downs
        postScore = submission.score
        postName = submission.name
        postTime = submission.created
        postNumComments = submission.num_comments
	
	fw1.write(str(i-1) + "," + str(postID) + "\t" + str(postAuthor) + "\t" + str(postTitle) + "\t" + str(postTime) + "\t" + str(postUps) + "\t" + str(postDown) + "\n")	
	
        postDic[postID] = {}
        postDic[postID]['post ID'] = postID
        postDic[postID]['post title'] = postTitle
        postDic[postID]['post body'] = postText
        postDic[postID]['post Author'] = postAuthor

        postDic[postID]['post time'] = postTime
        postDic[postID]['post URL'] = postUrl
        postDic[postID]['post subreddit'] = postSubreddit
        postDic[postID]['post ups'] = postUps
        postDic[postID]['post downs'] = postDown
        postDic[postID]['post score'] = postScore
        postDic[postID]['post num_comments'] = postNumComments
        postDic[postID]['cm'] = {}

        submission.comments.replace_more(limit=0)
        comment_queue = submission.comments[:]

        while comment_queue:
            cm= comment_queue.pop(0)

            if hasattr(cm, 'body'):
                commentBody=str(cm.body.encode('utf8'))
            else:
                cm.body=' '
            commentAuthor=str(cm.author)

            commentTime = cm.created
            commentUps = cm.ups
            commentDowns = cm.downs
            commentID = str(cm.id)
            commentName = str(cm.name)
            commentParentId = cm.parent_id
            commentSubreddit = str(cm.subreddit)
            cmStr = commentID

            postDic[postID]['cm'][cmStr] = {}
            postDic[postID]['cm'][cmStr]['comment ID'] = commentID
            postDic[postID]['cm'][cmStr]['comment ID of parrent'] = commentParentId
            postDic[postID]['cm'][cmStr]['comment name'] = commentName
            postDic[postID]['cm'][cmStr]['comment body'] = commentBody
            postDic[postID]['cm'][cmStr]['comment author'] = commentAuthor
            # postDic[postID]['cm'][cmStr]['comment author link_karma'] = commentAuthorLinkKarma
            # postDic[postID]['cm'][cmStr]['comment author comment_karma'] = commentAuthorCommentKarma
            postDic[postID]['cm'][cmStr]['comment time'] = commentTime
            postDic[postID]['cm'][cmStr]['comment subreddit'] = commentSubreddit
            postDic[postID]['cm'][cmStr]['comment ups'] = commentUps
            postDic[postID]['cm'][cmStr]['comment downs'] = commentDowns
            #PUT IT IN JSON
            path = "depression/" + postID + ".json"
            with open(path, "w") as writeJSON:
                json.dump(postDic, writeJSON)





            #for CSV file
            s=str(submission.selftext.encode('utf8'))
            c=str(cm.body.encode('utf8'))
            output_writer.writerow([s, c])
            comment_queue.extend(cm.replies)



    fw.close()
    fw1.close()


if __name__ == '__main__':
    main()
