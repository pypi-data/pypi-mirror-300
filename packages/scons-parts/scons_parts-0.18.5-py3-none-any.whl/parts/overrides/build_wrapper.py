# this overide deals with allowing Parts to record what targets file a given Parts/component
# will create. It also adds support for the generic allow_duplicate value for all builders
# which allows a builder call that is called twice and that build the same target for different
# environments to ignore that one set was built, avoiding the warning or error from SCons about
# building duplicate files. This is nice for copying config files that are platform independent
# during a cross build.


# I could try to turn the key into a string however i was unsure of speed impact..
# deal with that latter


import parts.errors as errors
import SCons.Builder
# we used lists as a dictionary can't take a tuple as a key
import SCons.Environment

key_list = []
value_list = []

Orig_call = SCons.Builder.BuilderBase.__call__

def parts_call_(self, env, target=None, source=None, chdir=SCons.Builder._null, **kw):
    try:
        #print(7776,target)
        targets = self.Orig_call(env, target, source, chdir=chdir, **kw)   
        # this was just a simple way to do this in a generic way
        # If we have DYN_SCANNER define in the env.. we want to add the node referenced
        #      
    except errors.AllowedDuplication as e:
        # this happens when we have match on the duplication key
        # the exeception has the targets to return
        #print(f"7777 DUPLICATE {e.targets}")
        targets = e.targets
    node = env.get('_DYNSCANNER_NODE')
    if node:
        for tg in targets:
            if not tg.isVisited:
                env.Depends(tg,node)

    return targets


SCons.Builder.BuilderBase.__call__ = parts_call_
SCons.Builder.BuilderBase.Orig_call = Orig_call

