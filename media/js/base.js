function isInstance(x, Obj){
    return Object.prototype.toString.call(x) === Object.prototype.toString.call(Obj);
}

var xhr = function(params){
    url = params.url;
    data = params.data || {};
    type = params.type || "GET";

    $.ajax(url, {
        dataType: params.dataType || "json",
        data: data,
        type: type,
        crossDomain: params.crossDomain || false,
        success: function(response, state, jqXHR){
            if (params.success) params.success(response, state);
        },
        error: function(response, state, jqXHR){
            if (params.failure) params.failure(response, state);
        },
        beforeSend: function(xhrResponse, settings){
            xhrResponse.setRequestHeader('X-Force-XHttpResponse', 'on');
            if (params.beforeSendHeaders){
                //[['header', 'value'], ['header2', 'value2'], ...]
                if (isInstance(params.beforeSendHeaders, [])){
                    params.beforeSendHeaders.map(function(header){
                        xhrResponse.setRequestHeader(header[0], header[1]);
                    });
                } else {  // X-HEADER=value
                    keyVal = params.beforeSendHeaders.split('=');
                    xhrResponse.setRequestHeader(keyVal[0], keyVal[1]);
                }
            }
        }
    });
}

var postAjax = function(params){
    params.type = 'POST';
    xhr(params);
}

var updateFormErrors = function(form, errors){
    $('ul.errors').detach().remove();
    for (el in errors){
        
        blk = $(form).find("#id_" + el);
        ul = $("<ul class='errors'></ul>");
        for (i=0; i < errors[el].length; i++){
            li = $("<li>" + errors[el][i] + "</li>");
            li.appendTo(ul);
        }
        ul.insertBefore(blk);
		blk.addClass('errors');
    }
}

var postFormAjax = function(p){
    form = p.form;
    data = p.data || form.serialize();

    postAjax({
        url: p.url || form.attr('action'),
        data: data,
        success: function(response, code){
            var _form = (typeof response.form == 'undefined') ? {} : response.form;
            if (_form.errors){
                updateFormErrors(form, _form.errors);
                $(form).find("input, select").removeAttr('disabled');
            }
            else {
                // do something
                var message = noty({
                    text: p.successMsg || "Сохранено ;)",
                    type: "success",
                    dismissQueue: true,
                    timeout: (typeof p.notyTimeout == 'undefined') ? 2000 : p.notyTimeout
                });
                if (p.reloadPage || false ){
                    setTimeout(function(){
                        document.location.reload();
                    }, p.reloadTimeout || 2500);
                }
                if (p.success) p.success(response);
            }
        },
        failure: function(response, code){
            noty({
                text: p.failreMsg || "Что-то пошло не так",
                type: "error",
                dismissQueue: true
            });
        }
    }); //end postAjax
}

var parseJSONFormFields = function(data, form){
    $.each(data, function(index, value){
        if (isInstance(value, [])){
            $.each(value, function(idx, val){
                if (!isInstance(value, [])){
                    container = "#id_" + index + ' option[value=' + val + ']';
                    $(form).find(container).attr({selected: true});
                }
            });//each value given array
        } else {
            if ($(form).find('#id_' + index).is('select')){
                $(form).find('#id_' + index).find('option[value='+value+']').attr({selected: true});
            } else {
                form.find('#id_' + index).attr({value: value});
            }// if given
        } // if isarray
    });// each
}
