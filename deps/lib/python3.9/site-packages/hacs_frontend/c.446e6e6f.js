import{_ as i,j as a,e as t,J as s,T as o,b as e,p as n,aE as r,r as l,n as d}from"./main-60575625.js";import"./c.386ba692.js";import"./c.d3dbc78b.js";import"./c.309b4815.js";import"./c.5325c693.js";import"./c.40bbc652.js";i([d("dialog-box")],(function(i,a){return{F:class extends a{constructor(...a){super(...a),i(this)}},d:[{kind:"field",decorators:[t({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[s()],key:"_params",value:void 0},{kind:"field",decorators:[s()],key:"_value",value:void 0},{kind:"method",key:"showDialog",value:async function(i){this._params=i,i.prompt&&(this._value=i.defaultValue)}},{kind:"method",key:"closeDialog",value:function(){var i,a;return!(null!==(i=this._params)&&void 0!==i&&i.confirmation||null!==(a=this._params)&&void 0!==a&&a.prompt)&&(!this._params||(this._dismiss(),!0))}},{kind:"method",key:"render",value:function(){if(!this._params)return o``;const i=this._params.confirmation||this._params.prompt;return o`
      <ha-dialog
        open
        ?scrimClickAction=${i}
        ?escapeKeyAction=${i}
        @closed=${this._dialogClosed}
        defaultAction="ignore"
        .heading=${this._params.title?this._params.title:this._params.confirmation&&this.hass.localize("ui.dialogs.generic.default_confirmation_title")}
      >
        <div>
          ${this._params.text?o`
                <p
                  class=${e({"no-bottom-padding":Boolean(this._params.prompt),warning:Boolean(this._params.warning)})}
                >
                  ${this._params.text}
                </p>
              `:""}
          ${this._params.prompt?o`
                <paper-input
                  dialogInitialFocus
                  .value=${this._value}
                  @keyup=${this._handleKeyUp}
                  @value-changed=${this._valueChanged}
                  .label=${this._params.inputLabel?this._params.inputLabel:""}
                  .type=${this._params.inputType?this._params.inputType:"text"}
                ></paper-input>
              `:""}
        </div>
        ${i&&o`
          <mwc-button @click=${this._dismiss} slot="secondaryAction">
            ${this._params.dismissText?this._params.dismissText:this.hass.localize("ui.dialogs.generic.cancel")}
          </mwc-button>
        `}
        <mwc-button
          @click=${this._confirm}
          ?dialogInitialFocus=${!this._params.prompt}
          slot="primaryAction"
        >
          ${this._params.confirmText?this._params.confirmText:this.hass.localize("ui.dialogs.generic.ok")}
        </mwc-button>
      </ha-dialog>
    `}},{kind:"method",key:"_valueChanged",value:function(i){this._value=i.detail.value}},{kind:"method",key:"_dismiss",value:function(){var i;null!==(i=this._params)&&void 0!==i&&i.cancel&&this._params.cancel(),this._close()}},{kind:"method",key:"_handleKeyUp",value:function(i){13===i.keyCode&&this._confirm()}},{kind:"method",key:"_confirm",value:function(){this._params.confirm&&this._params.confirm(this._value),this._close()}},{kind:"method",key:"_dialogClosed",value:function(i){"ignore"!==i.detail.action&&this._dismiss()}},{kind:"method",key:"_close",value:function(){this._params&&(this._params=void 0,n(this,"dialog-closed",{dialog:this.localName}))}},{kind:"get",static:!0,key:"styles",value:function(){return[r,l`
        :host([inert]) {
          pointer-events: initial !important;
          cursor: initial !important;
        }
        a {
          color: var(--primary-color);
        }
        p {
          margin: 0;
          padding-top: 6px;
          padding-bottom: 24px;
          color: var(--primary-text-color);
        }
        .no-bottom-padding {
          padding-bottom: 0;
        }
        .secondary {
          color: var(--secondary-text-color);
        }
        ha-dialog {
          /* Place above other dialogs */
          --dialog-z-index: 104;
        }
        .warning {
          color: var(--warning-color);
        }
      `]}}]}}),a);
