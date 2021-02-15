from flask import Flask, request, render_template, jsonify, url_for
from weblablib import WebLab, logout, poll, requires_active,requires_login, weblab_user
import hardware

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'something-random',
    'WEBLAB_USERNAME': 'weblabdeusto',
    'WEBLAB_PASSWORD': 'password',
})
weblab = WebLab(app)

@weblab.on_start
def start(client_data, server_data):
    print("inicializando {}".format(weblab_user))

@weblab.on_dispose
def dispose():
    print("Desechando {}".format(weblab_user))
    clean_resources()

@weblab.initial_url
def initial_url():
    return url_for('index')

@app.route('/logout')
@requires_active
def logout_view():
    logout()
    return jsonify(result='ok')

@app.route('/poll')
@requires_active
def poll():
    poll()
    return jsonify(result='ok')



#@app.route('/')
#@requires_login
#def index():
#    if weblab_user.active:
        # Show something for current users
#    else:
        # Show something for past users


@app.route('/')
@requires_login
def index():
    return render_template("lab.html")

@app.route('/status')
@requires_active
def status():
    return jsonify(lights=get_light_status(),
                   time_left=weblab_user.time_left,
                   error=False)

@app.route('/lights/<number>/')
@requires_active
def light(number):
    state = request.args.get('state') == 'true'
    hardware.switch_light(number, state)
    return jsonify(lights=get_light_status(),error=False)


def get_light_status():
    lights={}
    for light in range(1,11):
        lights['light-{}'.format(light)] = hardware.is_light_on(light)
    return lights

@app.cli.command('clean-resources')
def clean_resources_command():
    hardware.clean_resources()