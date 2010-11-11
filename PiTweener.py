# piTweener
# 
# Tweening functions for python
# 
# Heavily based on caurina Tweener: http://code.google.com/p/tweener/
# Forked from pyTweener:
# http://wiki.python-ogre.org/index.php/CodeSnippits_pyTweener
# 
# Released under the MIT License - see above url
# Original Python version by Ben Harling 2009
# Bugfixes and fork by Benjamin Woodruff 2010
# 
# 
# Copyright (c) Ben Harling (2009), Benjamin Woodruff (2010)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import math

class Tweener:
    def __init__(self):
        """Tweener
        This class manages all active tweens, and provides a factory for
        creating and spawning tween motions."""
        self.currentTweens = []
        self.defaultTweenType = self.IN_OUT_QUAD
        self.defaultDuration = 1.0
    
    def OUT_EXPO(self, t, b, c, d):
        if (t == d):
            return b + c
        return c * (-2 ** (-10 * t / d) + 1) + b;
    
    def LINEAR (self, t, b, c, d):
        return c * t / d + b
    
    def IN_QUAD (self, t, b, c, d):
        t /= d
        return c * t * t + b
    
    def OUT_QUAD (self, t, b, c, d):
        t /= d
        return -c * t * (t - 2) + b
    
    def IN_OUT_QUAD(self, t, b, c, d):
        t /= d * .5
        if t < 1.:
            return c * .5 * t * t + b
        t -= 1.
        return -c * .5 * (t * (t - 2.) - 1.) + b
    
    def OUT_IN_QUAD(self, t, b, c, d):
        if t < d * .5:
            return self.OUT_QUAD(t * 2, b, c * .5, d)
        return self.IN_QUAD(t * 2 - d, b + c * .5, c * .5)
    
    def IN_CUBIC(self, t, b, c, d):
        t /= d
        return c * t * t * t + b
    
    def OUT_CUBIC(self, t, b, c, d):
        t = t / d - 1
        return c * (t * t * t + 1) + b
    
    def IN_OUT_CUBIC(self, t, b, c, d):
        t /= d * .5
        if t < 1:
             return c * .5 * t * t * t + b
        t -= 2
        return c * .5 * (t * t * t + 2) + b
    
    def OUT_IN_CUBIC(self, t, b, c, d ):
        if t < d * .5:
        	return self.OUT_CUBIC (t * 2., b, c * .5, d)
        return self.IN_CUBIC(t * 2. - d, b + c * .5, c * .5, d)
    
    def IN_QUART(self, t, b, c, d):
        t /= d
        return c * t * t * t * t + b
    
    def OUT_QUART(self, t, b, c, d):
        t = t / d - 1
        return -c * ((t)*t*t*t - 1) + b
    
    def IN_OUT_QUART(self, t, b, c, d):
        t /= d * .5
        if t < 1: 
            return c * .5 * t * t * t * t + b
        t -= 2
        return -c / 2 * (t * t * t * t - 2) + b
    
    def OUT_ELASTIC(self, t, b, c, d):
        if t == 0: 
            return b
        t /= d
        if t == 1:
            return b + c
        p = d * .3 # period
        a = 1. # amplitude
        if a < abs(c):
            a = c
            s = p / 4
        else:
            s = p / (2. * math.pi) * math.asin(c / a)
        
        return (a * 2. ** (-10. * t) * math.sin((t * d - s) * (2. * math.pi)
                                                / p) + c + b)
    
    
    def hasTweens(self):
        return len(self.currentTweens) > 0
    
    
    def addTween(self, obj, **kwargs):
        """addTween(object, **kwargs) returns Tween object or False
           
           Example:
           tweener.addTween(myRocket, throttle=50, setThrust=400,
                            tweenTime=5.0, tweenType=tweener.OUT_QUAD)
           
           You must first specify an object, and at least one property or
           function with a corresponding change value. The tween will throw an
           error if you specify an attribute the object does not possess. Also
           the data types of the change and the initial value of the tweened
           item must match. If you specify a 'set' -type function, the tweener
           will attempt to get the starting value by call the corresponding
           'get' function on the object. If you specify a property, the tweener
           will read the current state as the starting value. You add both
           functions and property changes to the same tween.
           
           in addition to any properties you specify on the object, these
           keywords do additional setup of the tween.
           
           tweenTime = the duration of the motion
           tweenType = a predefined tweening equations or your own function
           onCompleteFunction = a function to call on completion of the tween
           onUpdateFunction = a function to call every time the tween updates
           tweenDelay = a delay before starting.
           """
        if "tweenTime" in kwargs:
            t_time = kwargs.pop("tweenTime")
        else:
            t_time = self.defaultDuration
        
        if "tweenType" in kwargs:
            t_type = kwargs.pop("tweenType")
        else:
            t_type = self.defaultTweenType
        
        if "onCompleteFunction" in kwargs:
            t_completeFunc = kwargs.pop("onCompleteFunction")
        else:
            t_completeFunc = None
        
        if "onUpdateFunction" in kwargs:
            t_updateFunc = kwargs.pop("onUpdateFunction")
        else:
            t_updateFunc = None
        
        if "tweenDelay" in kwargs:
            t_delay = kwargs.pop("tweenDelay")
        else:
            t_delay = 0
        
        tw = Tween(
            obj, t_time, t_type, t_completeFunc, t_updateFunc, t_delay, **kwargs
        )
        if tw:    
            self.currentTweens.append(tw)
        return tw
    
    def removeAllTweens(self):
        for i in self.currentTweens:
            i.complete = True
        self.currentTweens = []
    
    def removeTween(self, tweenObj):
        if tweenObj in self.currentTweens:
            tweenObj.complete = True
            self.currentTweens.remove(tweenObj)
    
    def getTweensAffectingObject(self, obj):
        """Get a list of all tweens acting on the specified object. Useful for
           manipulating tweens on the fly
           """
        tweens = []
        for t in self.currentTweens:
            if t.target is obj:
                tweens.append(t)
        return tweens
    
    def removeTweeningFrom(self, obj):
        """Stop tweening an object, without completing the motion or firing the
           completeFunction
           """
        # TODO: This loop could be optimized a bit
        for t in self.currentTweens[:]:
            if t.target is obj:
                t.complete = True
                self.currentTweens.remove(t)
    
    def update(self, timeSinceLastFrame):
        for t in self.currentTweens:
            t.update(timeSinceLastFrame)
            if t.complete:
                self.currentTweens.remove(t)


class Tween(object):
    def __init__(self, obj, tduration, tweenType, completeFunction,
                 updateFunction, delay, **kwargs):
        """Tween object:
           Can be created directly, but much more easily using
           Tweener.addTween(...)
           """
        self.duration = tduration
        self.delay = delay
        self.target = obj
        self.tween = tweenType
        self.tweenables = kwargs
        self.delta = 0
        self.completeFunction = completeFunction
        self.updateFunction = updateFunction
        self.complete = False
        self.tProps = []
        self.tFuncs = []
        self.paused = self.delay > 0
        self.decodeArguments()
    
    def decodeArguments(self):
        """Internal setup procedure to create tweenables and work out how to
           deal with each
           """
        
        if len(self.tweenables) == 0:
            # nothing to do 
            print "TWEEN ERROR: No Tweenable properties or functions defined"
            self.complete = True
            return
        
        
        for k, v in self.tweenables.items():
            
            # check that it's compatible
            if not hasattr(self.target, k):
                print \
                    "TWEEN ERROR: " + str(self.target) + " has no function " + k
                self.complete = True
                continue
            
            prop = func = False
            startVal = 0
            change = v
            
            var = getattr(self.target, k)
            if hasattr(var, "__call__"):
                func = var
                funcName = k
            else:
                startVal = var
                change = v-startVal
                prop = k
                propName = k
            
            
            if func:
                try:
                    getFunc = getattr(self.target,
                                      funcName.replace("set", "get"))
                    startVal = getFunc()
                    change = v-startVal
                except:
                    # no start value, assume its 0
                    # but make sure the start and change
                    # dataTypes match :)
                    startVal = change * 0
                tweenable = Tweenable(startVal, change)    
                newFunc = [k, func, tweenable]
                
                
                self.tFuncs.append(newFunc)
            
            
            if prop:
                tweenable = Tweenable(startVal, change)    
                newProp = [k, prop, tweenable]
                self.tProps.append(newProp)  
    
    
    def pause(self, numSeconds=-1):
        """Pause this tween
           do tween.pause(2) to pause for a specific time, or tween.pause()
           which pauses indefinitely.
           """
        self.paused = True
        self.delay = numSeconds
    
    def resume(self):
        "Resume from pause"
        if self.paused:
            self.paused=False
    
    def update(self, ptime):
        """Update this tween with the time since the last frame if there is an
           update function, it is always called whether the tween is running or
           paused
           """
        if self.paused:
            if self.delay > 0:
                self.delay = max(0, self.delay - ptime)
                if self.delay == 0:
                    self.paused = False
                    self.delay = -1
                if self.updateFunction:
                    self.updateFunction()
            return
        
        self.delta = min(self.delta + ptime, self.duration)
        
        if not self.complete:
            for propName, prop, tweenable in self.tProps:
                setattr(self.target, prop,
                        self.tween(self.delta, tweenable.startValue,
                                   tweenable.change, self.duration))
            for funcName, func, tweenable in self.tFuncs:
                func(
                    self.tween(self.delta, tweenable.startValue,
                               tweenable.change, self.duration)
                )
        
        
        if self.delta == self.duration:
            self.complete = True
            if self.completeFunction:
                self.completeFunction()
        
        if self.updateFunction:
            self.updateFunction()
    
    
    
    def getTweenable(self, name):
        """Return the tweenable values corresponding to the name of the original
        tweening function or property. 
        
        Allows the parameters of tweens to be changed at runtime. The parameters
        can even be tweened themselves!
        
        Eg:
        
        # the rocket needs to escape!! -- we're already moving, but must go
        # faster!
        twn = tweener.getTweensAffectingObject(myRocket)[0]
        tweenable = twn.getTweenable("thrusterPower")
        tweener.addTween(
            tweenable, change=1000.0, tweenTime=0.4, tweenType=tweener.IN_QUAD
        )
        """
        ret = None
        for n, f, t in self.tFuncs:
            if n == name:
                ret = t
                return ret
        for n, p, t in self.tProps:
            if n == name:
                ret = t
                return ret
        return ret
    
    
    
    
    def Remove(self):
        "Disables and removes this tween without calling the complete function"
        self.complete = True



class Tweenable:
    def __init__(self, start, change):
        """Tweenable:
            Holds values for anything that can be tweened
            these are normally only created by Tweens"""
        self.startValue = start
        self.change = change



class TweenTestObject:
    def __init__(self):
        self.pos = 20
        self.rot = 50
    
    def update(self):
        print self.pos, self.rot
    
    def setRotation(self, rot):
        self.rot = rot
    
    def getRotation(self):
        return self.rot
    
    def complete(self):
        print "I'm done tweening now mommy!"



if __name__=="__main__":
    import time
    T = Tweener()
    tst = TweenTestObject()
    mt = T.addTween(tst, tweenTime=2.5, tweenType=T.LINEAR, pos=-200,
                    onCompleteFunction=tst.complete,
                    onUpdateFunction=tst.update)
    s = time.time()
    changed = False
    while T.hasTweens():
        tm = time.time()
        d = tm - s
        s = tm
        T.update(d)
        time.sleep(.06)
    print "finished:"
    print tst.getRotation(), tst.pos

