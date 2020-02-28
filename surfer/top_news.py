from editor.models import NewsPost
import operator

def get_news():
    npl = NewsPost.objects.filter(pub_status=True)
    pop = []
    for np in npl:
        p = (np.like_no * 2) + np.view_no
        pop.append((np,p))
    pop.sort(key=operator.itemgetter(1),reverse=True)
    nnl = []
    i = 0
    for nl, v in pop:
        i+=1
        if i==5:
            break
        nnl.append(nl)
    return nnl