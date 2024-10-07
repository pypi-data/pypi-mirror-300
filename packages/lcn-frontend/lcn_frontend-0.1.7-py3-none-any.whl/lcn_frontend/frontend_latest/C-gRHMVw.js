export const id=646;export const ids=[646];export const modules={1646:(i,e,t)=>{var a=t(5461),o=t(8597),n=t(993),s=t(9760),l=t(9278),r=t(3167),d=t(9534),c=t(26),h=t(7950);let m;c.m.addInitializer((async i=>{await i.updateComplete;const e=i;e.dialog.prepend(e.scrim),e.scrim.style.inset=0,e.scrim.style.zIndex=0;const{getOpenAnimation:t,getCloseAnimation:a}=e;e.getOpenAnimation=()=>{var i,e;const a=t.call(void 0);return a.container=[...null!==(i=a.container)&&void 0!==i?i:[],...null!==(e=a.dialog)&&void 0!==e?e:[]],a.dialog=[],a},e.getCloseAnimation=()=>{var i,e;const t=a.call(void 0);return t.container=[...null!==(i=t.container)&&void 0!==i?i:[],...null!==(e=t.dialog)&&void 0!==e?e:[]],t.dialog=[],t}}));(0,a.A)([(0,n.EM)("ha-md-dialog")],(function(i,e){class a extends e{constructor(){super(),i(this),this.addEventListener("cancel",this._handleCancel),"function"!=typeof HTMLDialogElement&&(this.addEventListener("open",this._handleOpen),m||(m=t.e(331).then(t.bind(t,331)))),void 0===this.animate&&(this.quick=!0),void 0===this.animate&&(this.quick=!0)}}return{F:a,d:[{kind:"field",decorators:[(0,n.MZ)({attribute:"disable-cancel-action",type:Boolean})],key:"disableCancelAction",value(){return!1}},{kind:"field",key:"_polyfillDialogRegistered",value(){return!1}},{kind:"method",key:"_handleOpen",value:async function(i){var e;if(i.preventDefault(),this._polyfillDialogRegistered)return;this._polyfillDialogRegistered=!0,this._loadPolyfillStylesheet("/static/polyfills/dialog-polyfill.css");const t=null===(e=this.shadowRoot)||void 0===e?void 0:e.querySelector("dialog");(await m).default.registerDialog(t),this.removeEventListener("open",this._handleOpen),this.show()}},{kind:"method",key:"_loadPolyfillStylesheet",value:async function(i){const e=document.createElement("link");return e.rel="stylesheet",e.href=i,new Promise(((t,a)=>{var o;e.onload=()=>t(),e.onerror=()=>a(new Error(`Stylesheet failed to load: ${i}`)),null===(o=this.shadowRoot)||void 0===o||o.appendChild(e)}))}},{kind:"method",key:"_handleCancel",value:function(i){if(this.disableCancelAction){var e;i.preventDefault();const t=null===(e=this.shadowRoot)||void 0===e?void 0:e.querySelector("dialog .container");void 0!==this.animate&&(null==t||t.animate([{transform:"rotate(-1deg)","animation-timing-function":"ease-in"},{transform:"rotate(1.5deg)","animation-timing-function":"ease-out"},{transform:"rotate(0deg)","animation-timing-function":"ease-in"}],{duration:200,iterations:2}))}}},{kind:"field",static:!0,key:"styles",value(){return[...(0,d.A)(a,"styles",this),o.AH`
      :host {
        --md-dialog-container-color: var(--card-background-color);
        --md-dialog-headline-color: var(--primary-text-color);
        --md-dialog-supporting-text-color: var(--primary-text-color);
        --md-sys-color-scrim: #000000;

        --md-dialog-headline-weight: 400;
        --md-dialog-headline-size: 1.574rem;
        --md-dialog-supporting-text-size: 1rem;
        --md-dialog-supporting-text-line-height: 1.5rem;
      }

      :host([type="alert"]) {
        min-width: 320px;
      }

      :host(:not([type="alert"])) {
        @media all and (max-width: 450px), all and (max-height: 500px) {
          min-width: calc(
            100vw - env(safe-area-inset-right) - env(safe-area-inset-left)
          );
          max-width: calc(
            100vw - env(safe-area-inset-right) - env(safe-area-inset-left)
          );
          min-height: 100%;
          max-height: 100%;
          --md-dialog-container-shape: 0;
        }
      }

      :host ::slotted(ha-dialog-header) {
        display: contents;
      }

      slot[name="content"]::slotted(*) {
        padding: var(--dialog-content-padding, 24px);
      }
      .scrim {
        z-index: 10; // overlay navigation
      }
    `]}}]}}),c.m);h.T,h.N;(0,a.A)([(0,n.EM)("ha-dialog-header")],(function(i,e){return{F:class extends e{constructor(...e){super(...e),i(this)}},d:[{kind:"method",key:"render",value:function(){return o.qy`
      <header class="header">
        <div class="header-bar">
          <section class="header-navigation-icon">
            <slot name="navigationIcon"></slot>
          </section>
          <section class="header-content">
            <div class="header-title">
              <slot name="title"></slot>
            </div>
            <div class="header-subtitle">
              <slot name="subtitle"></slot>
            </div>
          </section>
          <section class="header-action-items">
            <slot name="actionItems"></slot>
          </section>
        </div>
        <slot></slot>
      </header>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return[o.AH`
        :host {
          display: block;
        }
        :host([show-border]) {
          border-bottom: 1px solid
            var(--mdc-dialog-scroll-divider-color, rgba(0, 0, 0, 0.12));
        }
        .header-bar {
          display: flex;
          flex-direction: row;
          align-items: flex-start;
          padding: 4px;
          box-sizing: border-box;
        }
        .header-content {
          flex: 1;
          padding: 10px 4px;
          min-width: 0;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }
        .header-title {
          font-size: 22px;
          line-height: 28px;
          font-weight: 400;
        }
        .header-subtitle {
          font-size: 14px;
          line-height: 20px;
          color: var(--secondary-text-color);
        }
        @media all and (min-width: 450px) and (min-height: 500px) {
          .header-bar {
            padding: 12px;
          }
        }
        .header-navigation-icon {
          flex: none;
          min-width: 8px;
          height: 100%;
          display: flex;
          flex-direction: row;
        }
        .header-action-items {
          flex: none;
          min-width: 8px;
          height: 100%;
          display: flex;
          flex-direction: row;
        }
      `]}}]}}),o.WF);t(9222);var p=t(8068),u=t(5538);(0,a.A)([(0,n.EM)("ha-button")],(function(i,e){return{F:class extends e{constructor(...e){super(...e),i(this)}},d:[{kind:"field",static:!0,key:"styles",value(){return[u.R,o.AH`
      ::slotted([slot="icon"]) {
        margin-inline-start: 0px;
        margin-inline-end: 8px;
        direction: var(--direction);
        display: block;
      }
      .mdc-button {
        height: var(--button-height, 36px);
      }
      .trailing-icon {
        display: flex;
      }
      .slot-container {
        overflow: var(--button-slot-container-overflow, visible);
      }
    `]}}]}}),p.$);(0,a.A)([(0,n.EM)("dialog-box")],(function(i,e){return{F:class extends e{constructor(...e){super(...e),i(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_closeState",value:void 0},{kind:"field",decorators:[(0,n.P)("ha-textfield")],key:"_textField",value:void 0},{kind:"field",decorators:[(0,n.P)("ha-md-dialog")],key:"_dialog",value:void 0},{kind:"method",key:"showDialog",value:async function(i){this._params=i}},{kind:"method",key:"closeDialog",value:function(){var i,e;return!(null!==(i=this._params)&&void 0!==i&&i.confirmation||null!==(e=this._params)&&void 0!==e&&e.prompt)&&(!this._params||(this._dismiss(),!0))}},{kind:"method",key:"render",value:function(){if(!this._params)return o.s6;const i=this._params.confirmation||this._params.prompt,e=this._params.title||this._params.confirmation&&this.hass.localize("ui.dialogs.generic.default_confirmation_title");return o.qy`
      <ha-md-dialog
        open
        .disableCancelAction=${i||!1}
        @closed=${this._dialogClosed}
        type="alert"
        aria-labelledby="dialog-box-title"
        aria-describedby="dialog-box-description"
      >
        <div slot="headline">
          <span .title=${e} id="dialog-box-title">
            ${this._params.warning?o.qy`<ha-svg-icon
                  .path=${"M12,2L1,21H23M12,6L19.53,19H4.47M11,10V14H13V10M11,16V18H13V16"}
                  style="color: var(--warning-color)"
                ></ha-svg-icon> `:o.s6}
            ${e}
          </span>
        </div>
        <div slot="content" id="dialog-box-description">
          ${this._params.text?o.qy` <p>${this._params.text}</p> `:""}
          ${this._params.prompt?o.qy`
                <ha-textfield
                  dialogInitialFocus
                  value=${(0,l.J)(this._params.defaultValue)}
                  .placeholder=${this._params.placeholder}
                  .label=${this._params.inputLabel?this._params.inputLabel:""}
                  .type=${this._params.inputType?this._params.inputType:"text"}
                  .min=${this._params.inputMin}
                  .max=${this._params.inputMax}
                ></ha-textfield>
              `:""}
        </div>
        <div slot="actions">
          ${i&&o.qy`
            <ha-button
              @click=${this._dismiss}
              ?dialogInitialFocus=${!this._params.prompt&&this._params.destructive}
            >
              ${this._params.dismissText?this._params.dismissText:this.hass.localize("ui.dialogs.generic.cancel")}
            </ha-button>
          `}
          <ha-button
            @click=${this._confirm}
            ?dialogInitialFocus=${!this._params.prompt&&!this._params.destructive}
            class=${(0,s.H)({destructive:this._params.destructive||!1})}
          >
            ${this._params.confirmText?this._params.confirmText:this.hass.localize("ui.dialogs.generic.ok")}
          </ha-button>
        </div>
      </ha-md-dialog>
    `}},{kind:"method",key:"_cancel",value:function(){var i;null!==(i=this._params)&&void 0!==i&&i.cancel&&this._params.cancel()}},{kind:"method",key:"_dismiss",value:function(){this._closeState="canceled",this._closeDialog(),this._cancel()}},{kind:"method",key:"_confirm",value:function(){var i;(this._closeState="confirmed",this._closeDialog(),this._params.confirm)&&this._params.confirm(null===(i=this._textField)||void 0===i?void 0:i.value)}},{kind:"method",key:"_closeDialog",value:function(){var i;(0,r.r)(this,"dialog-closed",{dialog:this.localName}),null===(i=this._dialog)||void 0===i||i.close()}},{kind:"method",key:"_dialogClosed",value:function(){this._closeState||((0,r.r)(this,"dialog-closed",{dialog:this.localName}),this._cancel()),this._closeState=void 0,this._params=void 0}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`
      :host([inert]) {
        pointer-events: initial !important;
        cursor: initial !important;
      }
      a {
        color: var(--primary-color);
      }
      p {
        margin: 0;
        color: var(--primary-text-color);
      }
      .no-bottom-padding {
        padding-bottom: 0;
      }
      .secondary {
        color: var(--secondary-text-color);
      }
      .destructive {
        --mdc-theme-primary: var(--error-color);
      }
      ha-textfield {
        width: 100%;
      }
    `}}]}}),o.WF)}};
//# sourceMappingURL=C-gRHMVw.js.map