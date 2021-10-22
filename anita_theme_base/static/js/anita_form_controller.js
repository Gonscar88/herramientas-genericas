odoo.define('anita_theme_base.form_controller', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var Dialog = require('web.Dialog');
    var core = require('web.core')

    var FormController = FormController.include({
        overlay: undefined,

        /**
         * @private
         * @param {OdooEvent} ev
         */
        _onButtonClicked: function (ev) {
            // stop the event's propagation as a form controller might have other
            // form controllers in its descendants (e.g. in a FormViewDialog)
            ev.stopPropagation();
            var self = this;
            var def;

            this._disableButtons();

            function saveAndExecuteAction() {
                return self.saveRecord(self.handle, {
                    stayInEdit: true,
                }).then(function () {
                    // we need to reget the record to make sure we have changes made
                    // by the basic model, such as the new res_id, if the record is
                    // new.
                    var record = self.model.get(ev.data.record.id);
                    return self._callButtonAction(attrs, record);
                });
            }

            function SaveAndReturnRecord() {
                return self.saveRecord(self.handle, {
                    stayInEdit: true,
                }).then(function () {
                    var record = self.model.get(ev.data.record.id);
                    var action = { type: 'ir.actions.act_window_close', infos: record }
                    return self.do_action(action, {})
                });
            }

            function SaveAndNotify(msg_name) {
                return self.saveRecord(self.handle, {
                    stayInEdit: true,
                }).then(function () {
                    var record = self.model.get(ev.data.record.id);
                    core.bus.trigger(msg_name, record);
                });
            }

            var attrs = ev.data.attrs;
            if (attrs.confirm) {
                def = new Promise(function (resolve, reject) {
                    Dialog.confirm(this, attrs.confirm, {
                        confirm_callback: saveAndExecuteAction,
                    }).on("closed", null, resolve);
                });
            } else if (attrs.special === 'cancel') {
                def = this._callButtonAction(attrs, ev.data.record);
            } else if (attrs.special === 'save_and_return') {
                // extend to save and retur record
                def = SaveAndReturnRecord();
            } else if (attrs.special === 'save_and_notify') {
                def = SaveAndNotify(attrs.name);
            } else if (!attrs.special || attrs.special === 'save') {
                // save the record but don't switch to readonly mode
                def = saveAndExecuteAction();
            } else {
                console.warn('Unhandled button event', ev);
                return;
            }

            // Kind of hack for FormViewDialog: button on footer should trigger the dialog closing
            // if the `close` attribute is set
            def.then(function () {
                self._enableButtons();
                if (attrs.close) {
                    self.trigger_up('close_dialog');
                }
            }).guardedCatch(this._enableButtons.bind(this));
        }
    })
})