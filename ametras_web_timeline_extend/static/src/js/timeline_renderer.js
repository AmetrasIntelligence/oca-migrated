odoo.define("ametras_web_timeline_extend.TimelineRenderer", function (require) {
    const TimelineRenderer = require("web_timeline.TimelineRenderer");
    const core = require("web.core");
    const time = require("web.time");

    const _t = core._t;

    TimelineRenderer.include({
        jsLibs: ["/web/static/lib/daterangepicker/daterangepicker.js"],
        cssLibs: ["/web/static/lib/daterangepicker/daterangepicker.css"],
        events: _.extend({}, TimelineRenderer.prototype.events, {
            "click .oe_timeline_button_previous": "_onButtonPreviousClicked",
            "click .oe_timeline_button_next": "_onButtonNextClicked",
        }),

        init: function (parent, state, params) {
            this._super.apply(this, arguments);
            this.dateRangePickerOptions = {
                timePicker: true,
                timePicker24Hour: true,
                timePickerIncrement: 5,
                timePickerSeconds: false,
                showWeekNumbers: true,
                startDate: moment(),
                endDate: moment().add(1, "days"),
                autoUpdateInput: true,
                locale: {
                    applyLabel: _t("Apply"),
                    cancelLabel: _t("Cancel"),
                    format: time.getLangDatetimeFormat(),
                },
            };
        },

        /**
         * @override
         */
        start: function () {
            this._super.apply(this, arguments);
            this.$dateRangePicker = this.$(".oe_timeline_range");
            this.$dateRangePicker.daterangepicker(this.dateRangePickerOptions);
            this.$el.on(
                "apply.daterangepicker",
                this._dateRangePickerApplyChanges.bind(this)
            );
            this._dateRangePickerPushParams();
        },

        /**
         * Apply changes from the daterangepicker on the timeline
         *
         * @private
         */
        _dateRangePickerApplyChanges: function (ev, picker) {
            this.current_window = {
                start: picker.startDate,
                end: picker.endDate,
            };
            this._updateWindowWithDates();
        },

        /**
         * Update preselected date and time values on the daterangepicker widget
         *
         * @private
         */
        _dateRangePickerPushParams: function () {
            // Set datepicker dates in widget
            this.$dateRangePicker
                .data("daterangepicker")
                .setStartDate(this.current_window.start);
            this.$dateRangePicker
                .data("daterangepicker")
                .setEndDate(this.current_window.end);
            // Resize input field to it's content
            this.$dateRangePicker.css(
                "width",
                this.$dateRangePicker.val().length + "ch"
            );
        },

        /**
         * Triggered when the timeline is attached to the DOM.
         */
        on_attach_callback: function () {
            const height =
                this.$el.parent().height() - this.$(".oe_timeline_buttons").height();
            if (height < this.min_height && this.timeline) {
                this.timeline.setOptions({
                    height: this.min_height,
                });
            }
        },

        /**
         * Set the timeline window to the previous time range.
         *
         * @private
         */
        _onButtonPreviousClicked: function () {
            var diff_days = this.current_window.end.diff(
                this.current_window.start,
                "days"
            );
            this.current_window = {
                start: this.current_window.start.subtract(diff_days, "days"),
                end: this.current_window.end.subtract(diff_days, "days"),
            };
            this._updateWindowWithDates();
        },

        /**
         * Set the timeline window to the next time range.
         *
         * @private
         */
        _onButtonNextClicked: function () {
            var diff_days = this.current_window.end.diff(
                this.current_window.start,
                "days"
            );
            this.current_window = {
                start: this.current_window.start.add(diff_days, "days"),
                end: this.current_window.end.add(diff_days, "days"),
            };
            this._updateWindowWithDates();
        },

        /**
         * Set the timeline window to today (day).
         *
         * @private
         */
        _onTodayClicked: function () {
            this.current_window = {
                start: new moment(),
                end: new moment().add(24, "hours"),
            };
            this._updateWindowWithDates();
        },

        /**
         * Update date range fields and timeline range.
         *
         * @private
         */
        _updateWindowWithDates: function () {
            // Set timeline windows range
            if (this.timeline) {
                this.timeline.setWindow(this.current_window);
            }
            // Push changes to daterange picker
            this._dateRangePickerPushParams();
        },

        /**
         * Scales the timeline window based on the current window.
         *
         * @param {Integer} factor The timespan (in hours) the window must be scaled to.
         * @private
         */
        _scaleCurrentWindow: function (factor) {
            if (this.timeline) {
                this.current_window = this.timeline.getWindow();
                this.current_window.start = moment(this.current_window.start);
                this.current_window.end = moment(this.current_window.start).add(
                    factor,
                    "hours"
                );
                this._updateWindowWithDates();
            }
        },

        /**
         * Set groups and events.
         *
         * @param {Object[]} events
         * @param {String[]} group_bys
         * @param {Boolean} adjust_window
         * @private
         */
        on_data_loaded_2: function (events, group_bys, adjust_window) {
            const data = [];
            this.grouped_by = group_bys;
            for (const evt of events) {
                if (evt[this.date_start]) {
                    data.push(this.event_data_transform(evt));
                }
            }
            const groups = this.split_groups(events, group_bys);
            this.timeline.setGroups(groups);
            this.timeline.setItems(data);
            const mode = !this.mode || this.mode === "fit";
            const adjust = _.isUndefined(adjust_window) || adjust_window;
            if (mode && adjust) {
                this.timeline.fit();
            }
        },

        /**
         * Get the groups.
         *
         * @param {Object[]} events
         * @param {String[]} group_bys
         * @private
         * @returns {Array}
         */
        split_groups: function (events, group_bys) {
            // Todo: Add support for nested groups
            // Todo: Only show unassigned group if needed
            if (group_bys.length === 0) {
                return events;
            }
            const groups = [];
            groups.push({id: -1, content: _t("Unassigned")});
            for (const evt of events) {
                const group_name = evt[_.first(group_bys)];
                if (group_name) {
                    if (group_name instanceof Array) {
                        const group = _.find(
                            groups,
                            (existing_group) => existing_group.id === group_name[0]
                        );
                        if (_.isUndefined(group)) {
                            groups.push({
                                id: group_name[0],
                                content: group_name[1],
                            });
                        }
                    }
                }
            }
            return groups;
        },
    });
});
