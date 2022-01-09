// patch for lower-version IE
if (! window.console) {
    window.console = {
        log: function() {},
        info: function() {},
        error: function() {},
        warn: function() {},
        debug: function() {}
    };
}

// patch for string.trim
if(! String.prototype.trim){
    String.prototype.trim = function() {
        return this.replace(/^\s+|\s+$/g, '');
    };
}

// patch for number.toDateTime
if(! Number.prototype.toDateTime) {
    var replaces = {
        'yyyy': function(dt) {
            return dt.getFullYear().toString();
        },
        'yy': function(dt) {
            return (dt.getFullYear() % 100).toString();
        },
        'MM': function(dt) {
            var m = dt.getMonth() + 1;
            return m<10 ? '0'+m : m.toString();
        },
        'M': function(dt) {
            var m = dt.getMonth() + 1;
            return m.toString();
        },
        'dd': function(dt) {
            var d = dt.getDate();
            return d < 10 ? '0' + d : d.toString();
        },
        'd': function(dt) {
            var d = dt.getDate();
            return d.toString();
        },
        'hh': function(dt) {
            var h = dt.getHours();
            return h < 10 ? '0' + h : h.toString();
        },
        'h': function(dt) {
            var h = dt.getHours();
            return h.toString();
        },
        'mm': function(dt) {
            var m = dt.getMinutes();
            return m < 10 ? '0' + m : m.toString();
        },
        'm': function(dt) {
            var m = dt.getMinutes();
            return m.toString();
        },
        'ss': function(dt) {
            var s = dt.getSeconds();
            return s < 10 ? '0' + s : s.toString();
        },
        's': function(dt) {
            var s = dt.getSeconds();
            return s.toString();
        },
        'a': function(dt) {
            var h = dt.getHours();
            return h<12 ? 'AM' : 'PM';
        }
    };
    var token = /([a-zA-Z]+)/;
    Number.prototype.toDateTime = function(format) {
        var fmt = format || 'yyyy-MM-dd hh:mm:ss';
        var dt = new Date(this * 1000);
        var arr = fmt.split(token);
        for(var i=0; i<arr.length; i++) {
            var s = arr[i];
            if(s && s in replaces) {
                arr[i] = replaces[s](dt);
            }
        }
        return arr.join('');
    };
}

function encodeHtml(str) {
    return String(str).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/'/g, '&#39;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

// extends jQuery.form
$(function() {
    console.log('Extends $from ...');
    $.fn.extend({
        showFormError: function (err) {
            return this.each(function() {
                var $form = $(this), $alert = $form && $form.find('.uk-alert-danger'), fieldName = err && err.data;
                if(! $form.is('form')) {
                    console.error('cannot call showFormError() on non-form object.');
                    return;
                }
                $form.find('input').removeClass('uk-form-danger');
                $form.find('select').removeClass('uk-form-danger');
                $form.find('textarea').removeClass('uk-form-danger');
                if($alert.length === 0) {
                    console.warn('Cannot find .uk_alert_danger element.');
                    return;
                }
                if(err) {
                    $alert.text(err.message ? err.message : (err.error ? err.error : err)).removeClass('uk-hidden').show();
                    if(($alert.offset().top - 60) < $(window).scrollTop()) {
                        $('html,body').animate({scrollTop: $alert.offset().top - 60});
                    }
                    if(fieldName) {
                        $form.find('[name='+fieldName+']').addClass('uk-form-danger');
                    }
                }
                else {
                    $alert.addClass('uk-hidden').hide();
                    $form.find('.uk-form-danger').removeClass('uk-form-danger');
                }
            });
        },
        showFormLoading: function(isLoading) {
            return this.each(function() {
                var $form = $(this), $submit = $form && $form.find('button[type=submit]'), $button = $form && $form.find('button');
                $i = $submit && $submit.find('i'), iconClass = $i && $i.attr('class');
                if(! $form.is('form')) {
                    console.error('Cannot call showFormLoading() on non-form object.');
                    return;
                }
                if(! iconClass || iconClass.indexOf('uk-icon') < 0) {
                    console.warn('Icon <i class="uk-icon:*" not found.');
                    return;
                }
                if(isLoading) {
                    $button.attr('disabled', 'disabled');
                    $i && $i.addClass('uk-spinner');
                }
                else {
                    $button.removeAttr('disabled');
                    $i && $i.removeClass('uk-spinner');
                }
            });
        },
        postJSON: function(url, data, callback) {
            if(arguments.length === 2) {
                callback = data;
                data = {};
            }
            return this.each(function() {
                var $form = $(this);
                $form.showFormError();
                $form.showFormLoading(true);
                _httpJSON('POST', url, data, function(err, r) {
                    if(err) {
                        $form.showFormError();
                        $form.showFormLoading(false);
                    }
                    callback && callback(err, r);
                });
            });
        }
    });
});

// ajax submit form
function _httpJSON(method, url, data, callback) {
    var opt = {
        type: method,
        dataType: 'json'
    };
    if(method === 'GET') {
        opt.utl = url + '?' + data;
    }
    if(method === 'POST') {
        opt.url = url;
        opt.data = JSON.stringify(data || {});
        opt.contentType = 'application/json';
    }
    $.ajax(opt).done(function(r) {
        if(r && r.error) {
            return callback(r);
        }
        return callback(null, r);
    }).fail(function(jqXHR, textStatus) {
        return callback({'error': 'http_bad_response', 'data': '' + jqXHR.status, 'message': 'Internet error(HTTP ' + jqXHR.status + ')'});
    });
}

function getJSON(url, data, callback) {
    if(arguments.length === 2) {
        callback = data;
        data = {};
    }
    if(typeof(data) === 'object') {
        var arr = [];
        $.each(data, function(k, v) {
            arr.push(k + '=' + encodeURIComponent(v));
        });
        data = arr.join('&');
    }
    _httpJSON('GET', url, data, callback);
}

function postJSON(url, data, callback) {
    if(arguments.length === 2) {
        callback = data;
        data = {};
    }
    _httpJSON('GET', url, data, callback);
}
