/**
 * Theme: Hyper - Responsive Bootstrap 4 Admin Dashboard
 * Author: Coderthemes
 * Component: Full-Calendar
 */

! function($) {
    "use strict";

    var CalendarApp = function() {
        this.$body = $("body")
        this.$modal = $('#event-modal'),
            this.$calendar = $('#calendar'),
            this.$formEvent = $("#form-event"),
            this.$btnNewEvent = $("#btn-new-event"),
            this.$btnDeleteEvent = $("#btn-delete-event"),
            this.$btnSaveEvent = $("#btn-save-event"),
            this.$modalTitle = $("#modal-title"),
            this.$calendarObj = null,
            this.$selectedEvent = null,
            this.$newEventData = null
    };


    /* on click on event */
    CalendarApp.prototype.onEventClick = function(info) {
            this.$formEvent[0].reset();
            this.$formEvent.removeClass("was-validated");
            this.$newEventData = null;
            this.$btnDeleteEvent.show();
            this.$modalTitle.text('Edit Event');
            this.$modal.modal({
                backdrop: 'static'
            });
            this.$selectedEvent = info.event;
            $("#event-title").val(this.$selectedEvent.title);
            $("#event-category").val(this.$selectedEvent.classNames[0]);
        },

        /* on select */
        CalendarApp.prototype.onSelect = function(info) {
            console.log("onSelect info", info);
            this.$formEvent[0].reset();
            this.$formEvent.removeClass("was-validated");

            this.$selectedEvent = null;
            this.$newEventData = info;
            this.$btnDeleteEvent.hide();
            this.$modalTitle.text('Add New Event');

            this.$modal.modal({
                backdrop: 'static'
            });
            this.$calendarObj.unselect();
        },

        /* Initializing */
        CalendarApp.prototype.init = function() {

            /*  Initialize the calendar  */
            var today = new Date($.now());

            var Draggable = FullCalendar.Draggable;
            var externalEventContainerEl = document.getElementById('external-events');

            var defaultEvents = [];
            var $this = this;
            // cal - init
            $this.$calendarObj = new FullCalendar.Calendar($this.$calendar[0], {
                slotDuration: '00:15:00',
                /* If we want to split day time each 15minutes */
                slotMinTime: '08:00:00',
                slotMaxTime: '19:00:00',
                themeSystem: 'bootstrap',
                bootstrapFontAwesome: false,
                buttonText: {
                    today: 'Today',
                    month: 'Month',
                    week: 'Week',
                    day: 'Day',
                    list: 'List',
                    prev: 'Prev',
                    next: 'Next'
                },
                initialView: 'dayGridMonth',
                handleWindowResize: true,
                height: $(window).height() - 200,
                headerToolbar: {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'dayGridMonth'
                },

                initialEvents: function(info, successCallback, failureCallback) {
                    var defaultEvents = [];
                    var $this = this;

                    function dateformat(date_str) {
                        var date = new Date(date_str);
                        var year = date.getFullYear();
                        var month = ("0" + (date.getMonth() + 1)).slice(-2);
                        var day = ("0" + date.getDate()).slice(-2);
                        var formatted_date = year + "-" + month + "-" + day;
                        return formatted_date;
                    }

                    $.ajax({
                        url: '/demo',
                        method: 'GET',
                        dataType: 'json',
                        success: function(data) {
                            var airplane = JSON.parse(data);
                            jQuery.each(airplane, function() {
                                defaultEvents.push({
                                    title: Number(this.maxcharge).toLocaleString() + "원",
                                    start: dateformat(this.date),
                                    end: dateformat(this.date),
                                    color: "#35b8e0"
                                }, {
                                    title: Number(this.avgcharge).toLocaleString() + "원",
                                    start: dateformat(this.date),
                                    end: dateformat(this.date),
                                    color: "#f9c851"
                                }, {
                                    title: Number(this.mincharge).toLocaleString() + "원",
                                    start: dateformat(this.date),
                                    end: dateformat(this.date),
                                    color: "#ff5b5b"
                                });
                            });
                            successCallback(defaultEvents);
                            // console.log("defaultEvents", defaultEvents);
                        },
                        error: function() {
                            // 데이터를 가져오는 도중 에러가 발생한 경우 실행되는 콜백 함수
                            console.log('Failed to fetch events data.');
                        }
                    });
                },
                editable: false,
                droppable: false, // this allows things to be dropped onto the calendar !!!
                // dayMaxEventRows: false, // allow "more" link when too many events
                selectable: true,
                dateClick: function(info) { $this.onSelect(info); },
                eventClick: function(info) { $this.onEventClick(info); }
            });

            $this.$calendarObj.render();

            // on new event button click
            $this.$btnNewEvent.on('click', function(e) {
                $this.onSelect({ date: new Date(), allDay: true });
            });

        },

        //init CalendarApp
        $.CalendarApp = new CalendarApp, $.CalendarApp.Constructor = CalendarApp

}(window.jQuery),

//initializing CalendarApp
function($) {
    "use strict";
    $.CalendarApp.init()
}(window.jQuery);