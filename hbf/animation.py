import pytweening as tween

def rise_and_bounce(object, height, speed):
    if object.animation == 'rise':
        # the rise is an exponential in
        offset = (height * tween.easeInExpo(object.step / height))
        object.rect.centery = object.pos.y - offset
        object.step += speed
        if object.step > height:
            object.step = 0
            object.animation = 'bounce'
    if object.animation == 'bounce':
        # 
        offset = height * tween.easeOutBounce(object.step / height)
        object.rect.centery = object.pos.y - height + offset
        object.step += speed
        if object.step > height:
            object.step = 0
            object.animation = 'rise'

#def damaged_flash(object, )