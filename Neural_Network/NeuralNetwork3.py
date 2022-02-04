import sys
import time
import numpy as npy
import csv

alpha = 0.02
epoch = 50

def sigactfn(n):
    n = npy.clip(n, -500, 500)
    return 1.0/(1.0+npy.exp(-n))

#derivative of sigmoid
def dsigactfn(n):
    s=sigactfn(n)
    return s*(1-s)


def softmax(n):
    x = npy.exp(n - n.max())
    return x / npy.sum(x,axis=1,keepdims=True)

def dsoftmax(n):
    x = npy.exp(n - n.max())
    return x/npy.sum(x,axis=0) * (1- x/npy.sum(x,axis=0))


#cross entropy loss function
def celf(a,b):
    return a-b 

#x is input i.e. image and y is output i.e. label

x1 = npy.genfromtxt('train_image2.csv', delimiter=",")
#print(x1)
x1/=255
#print(x1)
y1 = npy.genfromtxt('train_label2.csv', delimiter=",", dtype='int')

hoty = npy.zeros((y1.size, y1.max()+1))
hoty[npy.arange(y1.size), y1] = 1
hoty1 = hoty
#print(y1,hoty1)

x2 = npy.genfromtxt('test_image2.csv', delimiter=",")
#print(x2)
x2/=255
#print(x2)
y2 = npy.genfromtxt('test_label2.csv', delimiter=",", dtype='int')

hoty = npy.zeros((y2.size, y2.max()+1))
hoty[npy.arange(y2.size), y2] = 1
hoty2 = hoty


#with open("test.csv", "r") as ti:
#    data = list(csv.reader(ti, delimiter=","))
#print(npy.array(data, dtype = npy.float))

wandb = {'w1':npy.random.randn(784, 512) * npy.sqrt(1.0 / 784),
         'b1':npy.zeros((1,512)),
         'w2':npy.random.randn(512, 256) * npy.sqrt(1.0 / 512),
         'b2':npy.zeros((1, 256)),
         'w3':npy.random.randn(256, 10) * npy.sqrt(1.0 / 256),
         'b3':npy.zeros((1, 10))}

#for x,z in wandb.items():
  #  print(x,z)



stime = time.time()


for i in range(epoch):

    stime5=time.time()

    for a,b in zip(x1, hoty1):

        a=npy.array([a])
        b=npy.array([b])

        #print(a,b)

        #forward
        stime2=time.time()

        wandb['o0'] = a

        wandb['i1'] = npy.dot(wandb['o0'], wandb['w1']) + wandb['b1']
        wandb['o1'] = sigactfn(wandb['i1'])

        wandb['i2'] = npy.dot(wandb['o1'], wandb['w2']) + wandb['b2']
        wandb['o2'] = sigactfn(wandb['i2'])

        wandb['i3'] = npy.dot(wandb['o2'], wandb['w3']) + wandb['b3']
        wandb['o3'] = softmax(wandb['i3'])


        #print('forward',stime2-time.time())

        #backward

        stime3=time.time()
        adjust={}

        div = 50
        print(wandb['o3'])
        print()
        print(b)
        print('next')
        loss = celf(wandb['o3'],b) #/ wandb['o3'].shape[0] * dsoftmax(wandb['i3'])
        #print(loss)

        adjust['w3'] = npy.dot(wandb['o2'].T, loss)
        adjust['b3'] = npy.sum(loss, axis=1, keepdims=True)#/div

        los = npy.dot(loss,wandb['w3'].T) * dsigactfn(wandb['i2'])
        adjust['w2'] = npy.dot(wandb['o1'].T, los)
        adjust['b2'] = npy.sum(los, axis=1, keepdims=True)#/div

        lo = npy.dot(los,wandb['w2'].T) * dsigactfn(wandb['i1'])
        adjust['w1'] = npy.dot(wandb['o0'].T, lo)
        adjust['b1'] = npy.sum(lo, axis=1, keepdims=True)#/div

        #print('backward',stime3-time.time())

        #refinement

        stime4=time.time()


        for k,v in adjust.items():
            #print(k, wandb[k],end=' ')
            wandb[k] = wandb[k] - alpha * v
            #print(wandb[k])

        #print('refine',stime4-time.time())

    #accuracy

    pred = []
    #r=[]
    #forward
    for c,d in zip(x1, y1):

        c=npy.array([c])
        d=npy.array([d])
        #print(d)

        wandb['o0'] = c

        wandb['i1'] = npy.dot(wandb['o0'], wandb['w1']) + wandb['b1']
        wandb['o1'] = sigactfn(wandb['i1'])

        wandb['i2'] = npy.dot(wandb['o1'], wandb['w2']) + wandb['b2']
        wandb['o2'] = sigactfn(wandb['i2'])

        wandb['i3'] = npy.dot(wandb['o2'], wandb['w3']) + wandb['b3']
        wandb['o3'] = softmax(wandb['i3'])

        #print(wandb['o3'])  
        k = npy.argmax(wandb['o3'])
        #r.append(k)
        #print(k,k==d)
        pred.append(k==d)
    print(npy.mean(pred))
    #print('epoch',time.time()-stime5)
    


#test
#pred = []
r=[]
#forward
for a,b in zip(x2, y2):

    a=npy.array([a])
    b=npy.array([b])
       
    wandb['o0'] = a

    wandb['i1'] = npy.dot(wandb['o0'], wandb['w1']) + wandb['b1']
    wandb['o1'] = sigactfn(wandb['i1'])

    wandb['i2'] = npy.dot(wandb['o1'], wandb['w2']) + wandb['b2']
    wandb['o2'] = sigactfn(wandb['i2'])

    wandb['i3'] = npy.dot(wandb['o2'], wandb['w3']) + wandb['b3']
    wandb['o3'] = softmax(wandb['i3'])

        
    k = npy.argmax(wandb['o3'])
    r.append(k)
    print(k,r)
    #pred.append(k==npy.argmax(b))
#print(npy.mean(pred))

print('total',time.time()-stime)
npy.savetxt('test_predictions.csv', r, delimiter='\n')