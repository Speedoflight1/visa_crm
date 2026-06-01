/** @odoo-module **/

/*
 * "notes_popover" field widget.
 * Shows a short preview of a text field in the list. Clicking the preview opens
 * a popover with the full note text WITHOUT opening the record (the click is
 * stopped from bubbling to the row).
 */

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { usePopover } from "@web/core/popover/popover_hook";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class NotesPopoverContent extends Component {
    static template = "visa_ux.NotesPopoverContent";
    static props = ["text", "close?"];
}

export class NotesPopoverField extends Component {
    static template = "visa_ux.NotesPopoverField";
    static props = { ...standardFieldProps };

    setup() {
        this.popover = usePopover(NotesPopoverContent);
    }

    get text() {
        return this.props.record.data[this.props.name] || "";
    }

    get preview() {
        const t = this.text.replace(/\s+/g, " ").trim();
        if (!t) {
            return "—";
        }
        return t.length > 45 ? t.slice(0, 45) + "…" : t;
    }

    onClick(ev) {
        ev.stopPropagation();
        if (!this.text) {
            return;
        }
        this.popover.open(ev.currentTarget, { text: this.text });
    }
}

export const notesPopoverField = {
    component: NotesPopoverField,
    displayName: "Notes Preview",
    supportedTypes: ["text", "char"],
};

registry.category("fields").add("notes_popover", notesPopoverField);
