export const id=292;export const ids=[292];export const modules={7292:(t,e,i)=>{i.r(e),i.d(e,{LCNEntitiesPage:()=>f});var n=i(5461),a=i(9534),s=i(8597),o=i(993),d=(i(8842),i(2052),i(1424),i(4392),i(9222),i(7661),i(6396),i(5081)),l=i(7222),r=i(3407);const c="M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z";(0,n.A)([(0,o.EM)("lcn-entities-data-table")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"lcn",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"device",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"entities",value(){return[]}},{kind:"field",key:"_entities",value(){return(0,d.A)((t=>t.map((t=>({...t,delete:t})))))}},{kind:"field",key:"_columns",value(){return(0,d.A)((t=>t?{name:{title:this.lcn.localize("name"),sortable:!0,direction:"asc"},delete:{title:"",sortable:!1,minWidth:"80px",template:t=>s.qy`
                  <ha-icon-button
                    title=${this.lcn.localize("dashboard-entities-table-delete")}
                    .path=${c}
                    @click=${e=>this._onEntityDelete(e,t)}
                  ></ha-icon-button>
                `}}:{name:{title:this.lcn.localize("name"),sortable:!0,direction:"asc",minWidth:"35%"},domain:{title:this.lcn.localize("domain"),sortable:!0,minWidth:"25%"},resource:{title:this.lcn.localize("resource"),sortable:!0,minWidth:"25%"},delete:{title:"",sortable:!1,minWidth:"80px",template:t=>s.qy`
                  <ha-icon-button
                    title=${this.lcn.localize("dashboard-entities-table-delete")}
                    .path=${c}
                    @click=${e=>this._onEntityDelete(e,t)}
                  ></ha-icon-button>
                `}}))}},{kind:"method",key:"render",value:function(){return s.qy`
      <ha-data-table
        .hass=${this.hass}
        .columns=${this._columns(this.narrow)}
        .data=${this._entities(this.entities)}
        .noDataText=${this.lcn.localize("dashboard-entities-table-no-data")}
        .dir=${(0,l.Vc)(this.hass)}
        auto-height
        clickable
      ></ha-data-table>
    `}},{kind:"method",key:"_onEntityDelete",value:async function(t,e){t.stopPropagation(),await(0,r.$b)(this.hass,this.lcn.config_entry,e),this.dispatchEvent(new CustomEvent("lcn-configuration-changed",{bubbles:!0,composed:!0}))}}]}}),s.WF);var h=i(3167);const u=()=>Promise.all([i.e(746),i.e(578),i.e(811),i.e(334)]).then(i.bind(i,334));let f=(0,n.A)([(0,o.EM)("lcn-entities-page")],(function(t,e){class i extends e{constructor(...e){super(...e),t(this)}}return{F:i,d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"lcn",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"route",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Array,reflect:!1})],key:"tabs",value(){return[]}},{kind:"field",decorators:[(0,o.wk)()],key:"_deviceConfig",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_entityConfigs",value(){return[]}},{kind:"method",key:"firstUpdated",value:async function(t){(0,a.A)(i,"firstUpdated",this,3)([t]),u(),await this._fetchEntities(this.lcn.config_entry,this.lcn.address)}},{kind:"method",key:"render",value:function(){return this._deviceConfig||0!==this._entityConfigs.length?s.qy`
      <hass-tabs-subpage
        .hass=${this.hass}
        .narrow=${this.narrow}
        .route=${this.route}
        .tabs=${this.tabs}
      >
        <span slot="header"> ${this.lcn.localize("dashboard-entities-title")} </span>
        <ha-config-section .narrow=${this.narrow}>
          <span slot="introduction"> ${this.renderIntro()} </span>

          <ha-card
            header="${this._deviceConfig.address[2]?this.lcn.localize("dashboard-entities-entities-for-group"):this.lcn.localize("dashboard-entities-entities-for-module")}:
              (${this.lcn.config_entry.title}, ${this._deviceConfig.address[0]},
              ${this._deviceConfig.address[1]})
              ${this._deviceConfig.name?" - "+this._deviceConfig.name:""}
            "
          >
            <lcn-entities-data-table
              .hass=${this.hass}
              .lcn=${this.lcn}
              .entities=${this._entityConfigs}
              .device=${this._deviceConfig}
              .narrow=${this.narrow}
              @lcn-configuration-changed=${this._configurationChanged}
            ></lcn-entities-data-table>
          </ha-card>
        </ha-config-section>
        <ha-fab
          slot="fab"
          @click=${this._addEntity}
          .label=${this.lcn.localize("dashboard-entities-add")}
          extended
        >
          <ha-svg-icon slot="icon" path=${"M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"}></ha-svg-icon>
        </ha-fab>
      </hass-tabs-subpage>
    `:s.qy` <hass-loading-screen></hass-loading-screen> `}},{kind:"method",key:"renderIntro",value:function(){return s.qy`
      <h3>${this.lcn.localize("dashboard-entities-introduction")}</h3>
      <details>
        <summary>${this.lcn.localize("more-help")}</summary>
        <ul>
          <li>${this.lcn.localize("dashboard-entities-introduction-help-1")}</li>
          <li>${this.lcn.localize("dashboard-entities-introduction-help-2")}</li>
          <li>${this.lcn.localize("dashboard-entities-introduction-help-3")}</li>
          <li>${this.lcn.localize("dashboard-entities-introduction-help-4")}</li>
          <li>${this.lcn.localize("dashboard-entities-introduction-help-5")}</li>
        </ul>
      </details>
    `}},{kind:"method",key:"_configurationChanged",value:function(){this._fetchEntities(this.lcn.config_entry,this.lcn.address)}},{kind:"method",key:"_fetchEntities",value:async function(t,e){const i=(await(0,r.Uc)(this.hass,t)).find((t=>t.address[0]===e[0]&&t.address[1]===e[1]&&t.address[2]===e[2]));void 0!==i&&(this._deviceConfig=i),this._entityConfigs=await(0,r.U3)(this.hass,t,e)}},{kind:"method",key:"_addEntity",value:async function(){var t,e;t=this,e={lcn:this.lcn,device:this._deviceConfig,createEntity:async t=>!!(await(0,r.d$)(this.hass,this.lcn.config_entry,t))&&(await this._fetchEntities(this.lcn.config_entry,this.lcn.address),!0)},(0,h.r)(t,"show-dialog",{dialogTag:"lcn-create-entity-dialog",dialogImport:u,dialogParams:e})}}]}}),s.WF)}};
//# sourceMappingURL=aH5chG22.js.map