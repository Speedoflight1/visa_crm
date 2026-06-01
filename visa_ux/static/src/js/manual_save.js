/** @odoo-module **/

/*
 * ServiceNow-style manual save for leads.
 * Stops Odoo from silently auto-saving a dirty lead when you flip through the
 * record pager, switch menus, or change browser tab. The user must click the
 * Save (cloud) button to persist; otherwise they are asked to discard.
 * Scoped to crm.lead only so the rest of Odoo behaves normally.
 */

import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";

const MANUAL_SAVE_MODELS = ["crm.lead"];

patch(FormController.prototype, {
    _visaManualSave() {
        return MANUAL_SAVE_MODELS.includes(this.props.resModel);
    },

    _visaConfirmDiscard(message) {
        return new Promise((resolve) => {
            this.dialogService.add(ConfirmationDialog, {
                title: _t("Unsaved changes"),
                body: message,
                confirmLabel: _t("Discard changes"),
                confirm: () => resolve(true),
                cancelLabel: _t("Keep editing"),
                cancel: () => resolve(false),
            });
        });
    },

    async beforeLeave() {
        if (this._visaManualSave()) {
            if (this.model.root.dirty && !this.allowLeavingWithoutSaving) {
                const discard = await this._visaConfirmDiscard(
                    _t(
                        "This lead has changes that are NOT saved. Click the Save button to keep them. Discard the changes and leave?"
                    )
                );
                if (discard) {
                    await this.model.root.discard();
                    return true;
                }
                return false; // block navigation, stay on the lead
            }
            return true;
        }
        return super.beforeLeave(...arguments);
    },

    async onPagerUpdate({ offset, resIds }) {
        if (this._visaManualSave()) {
            const dirty = await this.model.root.isDirty();
            if (dirty) {
                const discard = await this._visaConfirmDiscard(
                    _t(
                        "This lead has changes that are NOT saved. Save them first, or discard to move to the next record."
                    )
                );
                if (!discard) {
                    return; // stay on the current record
                }
                await this.model.root.discard();
            }
            return this.model.load({ resId: resIds[offset] });
        }
        return super.onPagerUpdate(...arguments);
    },

    beforeVisibilityChange() {
        if (this._visaManualSave()) {
            return; // never auto-save just because the browser tab lost focus
        }
        return super.beforeVisibilityChange(...arguments);
    },
});
