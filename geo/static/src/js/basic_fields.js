odoo.define('geo.basic_fields', function (require) {
"use strict";

    var AbstractField = require('web.AbstractField');
    var registry = require('web.field_registry');
    var utils = require('web.utils');
    var core = require('web.core');
    var framework = require('web.framework');
    var session = require('web.session');
    var field_utils = require('web.field_utils');
    var AbstractFieldBinary = require('web.basic_fields').AbstractFieldBinary;

    var qweb = core.qweb;
    var _t = core._t;
    var _lt = core._lt;

    var GeoFieldBinaryFile = AbstractFieldBinary.extend({
        description: _lt("File"),
        template: 'GeoFieldBinaryFile',
        events: _.extend({}, AbstractFieldBinary.prototype.events, {
            'click': function (event) {
                if (this.mode === 'readonly' && this.value && this.recordData.id) {
                    this._onPreviewClick();
                }
            },
            'click .o_input': function () { // eq[0]
                this.$('.o_input_file').click();
            },
            'click .o_preview_file_button': '_onPreviewBtnClick',
        }),
        supportedFieldTypes: ['binary'],
        /**
         * @private
         * @param {string} [fileURI] file URI if specified
         * @returns {string} the pdf viewer URI
         */
        _getURI: function (fileURI) {
            var page = this.recordData[this.name + '_page'] || 1;
            if (!fileURI) {
                var queryObj = {
                    model: this.model,
                    field: this.name,
                    id: this.res_id,
                };
                var queryString = $.param(queryObj);
                fileURI = '/web/content?' + queryString;
            }
            fileURI = encodeURIComponent(fileURI);
            var viewerURL = '/web/static/lib/pdfjs/web/viewer.html?file=';
            return viewerURL + fileURI + '#page=' + page;
        },
        init: function () {
            this._super.apply(this, arguments);
            this.filename_value = this.recordData[this.attrs.filename];
            this.fileURI;
        },
        _renderReadonly: function () {
            this.do_toggle(!!this.value);
            if (this.value) {
                this.$el.empty().append($("<span/>").addClass('fa fa-file-pdf-o'));
                if (this.recordData.id) {
                    this.$el.css('cursor', 'pointer');
                } else {
                    this.$el.css('cursor', 'not-allowed');
                }
                if (this.filename_value) {
                    this.$el.append(" " + this.filename_value);
                }
            }
            if (!this.res_id) {
                this.$el.css('cursor', 'not-allowed');
            } else {
                this.$el.css('cursor', 'pointer');
            }
        },
        _renderEdit: function () {
            if (this.value) {
                this.$el.children().removeClass('o_hidden');
                this.$('.o_select_file_button').first().addClass('o_hidden');
                this.$('.o_input').eq(0).val(this.filename_value || this.value);
            } else {
                this.$el.children().addClass('o_hidden');
                this.$('.o_select_file_button').first().removeClass('o_hidden');
            }
        },
        _onPreviewClick: function () {
            var self = this;
            self.do_action({
                name: 'preview Actions',
                type: 'ir.actions.act_url',
                target: 'new',
                url: this._getURI(),
            });
        },
        _onPreviewBtnClick: function () {
            var self = this;
            self.do_action({
                name: 'preview Actions',
                type: 'ir.actions.act_url',
                target: 'new',
                url: this._getURI(this.fileURI),
            });
        },
        set_filename: function (value) {
            this._super.apply(this, arguments);
            this.filename_value = value; // will be used in the re-render
            // the filename being edited but not yet saved, if the user clicks on
            // download, he'll get the file corresponding to the current value
            // stored in db, which isn't the one whose filename is displayed in the
            // input, so we disable the download button
            this.$('.o_save_file_button').prop('disabled', true);
        },
        on_save_as: function (ev) {
            if (!this.value) {
                this.do_warn(false, _t("The field is empty, there's nothing to save."));
                ev.stopPropagation();
            } else if (this.res_id) {
                framework.blockUI();
                var filename_fieldname = this.attrs.filename;
                this.getSession().get_file({
                    complete: framework.unblockUI,
                    data: {
                        'model': this.model,
                        'id': this.res_id,
                        'field': this.name,
                        'filename_field': filename_fieldname,
                        'filename': this.recordData[filename_fieldname] || "",
                        'download': true,
                        'data': utils.is_bin_size(this.value) ? null : this.value,
                    },
                    error: (error) => this.call('crash_manager', 'rpc_error', error),
                    url: '/web/content',
                });
                ev.stopPropagation();
            }
        },
        on_file_change: function (ev) {
            this._super.apply(this, arguments);
            var files = ev.target.files;
            if (!files || files.length === 0) {
                return;
            }
            var fileURI = URL.createObjectURL(files[0]);
            this.fileURI = fileURI;
        },
    });

    var GeoFieldBinaryImage = AbstractFieldBinary.extend({
        description: _lt("Image"),
        fieldDependencies: _.extend({}, AbstractFieldBinary.prototype.fieldDependencies, {
            __last_update: {type: 'datetime'},
        }),
        template: 'GeoFieldBinaryImage',
        placeholder: "/web/static/src/img/placeholder.png",
        events: _.extend({}, AbstractFieldBinary.prototype.events, {
            'click': function (event) {
                if (this.mode === 'readonly' && this.value && this.recordData.id) {
                    this._onPreviewClick();
                }
            },
            'click .o_preview_img_button': '_onPreviewClick',
        }),
        supportedFieldTypes: ['binary'],
        file_type_magic_word: {
            '/': 'jpg',
            'R': 'gif',
            'i': 'png',
            'P': 'svg+xml',
        },
        accepted_file_extensions: 'image/*',
        _getImageUrl: function (model, res_id, field, unique) {
            return session.url('/web/image', {
                model: model,
                id: JSON.stringify(res_id),
                field: field,
                // unique forces a reload of the image when the record has been updated
                unique: field_utils.format.datetime(unique).replace(/[^0-9]/g, ''),
            });
        },
        init: function () {
            this._super.apply(this, arguments);
            this.filename_value = this.recordData[this.attrs.filename];
            this.fileURI;
        },
        set_filename: function (value) {
            this._super.apply(this, arguments);
            this.filename_value = value; // will be used in the re-render
            // the filename being edited but not yet saved, if the user clicks on
            // download, he'll get the file corresponding to the current value
            // stored in db, which isn't the one whose filename is displayed in the
            // input, so we disable the download button
            this.$('.o_save_file_button').prop('disabled', true);
        },
        _renderReadonly: function () {
            this.do_toggle(!!this.value);
            if (this.value) {
                this.$el.empty().append($("<span/>").addClass('fa fa-file-image-o'));
                if (this.recordData.id) {
                    this.$el.css('cursor', 'pointer');
                } else {
                    this.$el.css('cursor', 'not-allowed');
                }
                if (this.filename_value) {
                    this.$el.append(" " + this.filename_value);
                }
            }
            if (!this.res_id) {
                this.$el.css('cursor', 'not-allowed');
            } else {
                this.$el.css('cursor', 'pointer');
            }
        },
        _renderEdit: function () {
            if (this.value) {
                this.$el.children().removeClass('o_hidden');
                this.$('.o_select_file_button').first().addClass('o_hidden');
                this.$('.o_input').eq(0).val(this.filename_value || this.value);
            } else {
                this.$el.children().addClass('o_hidden');
                this.$('.o_select_file_button').first().removeClass('o_hidden');
            }
        },
        _onPreviewClick: function () {
            var self = this;
            var url = this.placeholder;
            if (this.value) {
                if (!utils.is_bin_size(this.value)) {
                    // Use magic-word technique for detecting image type
                    url = 'data:image/' + (this.file_type_magic_word[this.value[0]] || 'png') + ';base64,' + this.value;
                    var new_window = window.open("", "图片预览");
                    var new_img = new_window.document.createElement("img");
                    new_img.src = url;
                    new_window.document.body.setAttribute("style", "margin: 0px;background: #0e0e0e;height: 100%;");
                    new_window.document.body.appendChild(new_img);
                } else {
                    var field = this.nodeOptions.preview_image || this.name;
                    var unique = this.recordData.__last_update;
                    url = this._getImageUrl(this.model, this.res_id, field, unique);
                    self.do_action({
                        name: 'preview Image',
                        type: 'ir.actions.act_url',
                        target: 'new',
                        url: url,
                    });
                }
            }
        },
    });


    registry
        .add('geo_pdf_viewer', GeoFieldBinaryFile)
        .add('geo_img_viewer', GeoFieldBinaryImage);

    return {
        GeoFieldBinaryFile: GeoFieldBinaryFile,
        GeoFieldBinaryImage: GeoFieldBinaryImage
    };
});