/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, useState } from "@odoo/owl";

export class VisaCrmDashboard extends Component {
    static template = "visa_ux.Dashboard";
    static props = ["*"];

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({
            loading: true,
            total: 0,
            stages: [],
            hot: 0,
            followToday: 0,
            maxStage: 1,
        });
        onWillStart(() => this.load());
    }

    get _today() {
        return new Date().toISOString().slice(0, 10);
    }

    async load() {
        const groups = await this.orm.readGroup(
            "crm.lead",
            [["type", "=", "opportunity"]],
            ["stage_id"],
            ["stage_id"]
        );
        const stages = groups.map((g) => ({
            id: g.stage_id ? g.stage_id[0] : false,
            name: g.stage_id ? g.stage_id[1] : "Undefined",
            count: g.__count ?? g.stage_id_count ?? 0,
        }));
        const total = stages.reduce((a, s) => a + s.count, 0);
        const maxStage = Math.max(1, ...stages.map((s) => s.count));

        const hot = await this.orm.searchCount("crm.lead", [
            ["type", "=", "opportunity"],
            ["lead_temperature", "=", "hot"],
        ]);
        const followToday = await this.orm.searchCount("crm.lead", [
            ["follow_up_date", "<=", this._today],
            ["follow_up_date", "!=", false],
        ]);

        Object.assign(this.state, {
            loading: false,
            total,
            stages,
            hot,
            followToday,
            maxStage,
        });
    }

    barWidth(count) {
        return Math.round((count / this.state.maxStage) * 100);
    }

    _open(name, domain) {
        this.action.doAction({
            type: "ir.actions.act_window",
            name,
            res_model: "crm.lead",
            domain,
            views: [
                [false, "list"],
                [false, "form"],
            ],
            target: "current",
        });
    }

    openStage(stageId) {
        const domain = [["type", "=", "opportunity"]];
        if (stageId) {
            domain.push(["stage_id", "=", stageId]);
        }
        this._open("Leads", domain);
    }

    openHot() {
        this._open("Hot Leads", [
            ["type", "=", "opportunity"],
            ["lead_temperature", "=", "hot"],
        ]);
    }

    openFollowToday() {
        this._open("Today's Follow-ups", [
            ["follow_up_date", "<=", this._today],
            ["follow_up_date", "!=", false],
        ]);
    }
}

registry.category("actions").add("visa_crm_dashboard", VisaCrmDashboard);
