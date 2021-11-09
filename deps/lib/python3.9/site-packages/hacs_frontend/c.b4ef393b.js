import{_ as o,H as t,e as i,k as e,y as r,b as a,N as s,O as n,Q as d,R as c,c as l,h as p,r as h,n as m}from"./main-add588c4.js";import"./c.43f4ad5b.js";import"./c.2f022d00.js";import"./c.982728cb.js";import"./c.f637898d.js";import{a as u}from"./c.0a038163.js";import"./c.247b03d8.js";import"./c.09bd0fdb.js";import{b as y}from"./c.44802ffe.js";import"./c.eb1f5cc8.js";import"./c.9ac2453b.js";import"./c.e0b9a1d2.js";import"./c.a8d8c686.js";import"./c.9f27b448.js";let v=o([m("hacs-custom-repositories-dialog")],(function(o,t){return{F:class extends t{constructor(...t){super(...t),o(this)}},d:[{kind:"field",decorators:[i()],key:"_inputRepository",value:void 0},{kind:"field",decorators:[i()],key:"_error",value:void 0},{kind:"field",decorators:[e("#add-input")],key:"_addInput",value:void 0},{kind:"field",decorators:[e("#category")],key:"_addCategory",value:void 0},{kind:"method",key:"shouldUpdate",value:function(o){return o.has("narrow")||o.has("active")||o.has("_error")||o.has("repositories")}},{kind:"method",key:"render",value:function(){var o,t;if(!this.active)return r``;const i=null===(o=this.repositories)||void 0===o?void 0:o.filter(o=>o.custom);return r`
      <hacs-dialog
        .active=${this.active}
        .hass=${this.hass}
        .title=${this.hacs.localize("dialog_custom_repositories.title")}
        hideActions
      >
        <div class="content">
          <div class="list">
            ${null!==(t=this._error)&&void 0!==t&&t.message?r`<ha-alert alert-type="error" .rtl=${u(this.hass)}>
                  ${this._error.message}
                </ha-alert>`:""}
            ${null==i?void 0:i.filter(o=>this.hacs.configuration.categories.includes(o.category)).map(o=>r`<paper-icon-item>
                  ${"integration"===o.category?r`
                        <img
                          loading="lazy"
                          .src=${y({domain:o.domain,darkOptimized:this.hass.themes.darkMode,type:"icon"})}
                          referrerpolicy="no-referrer"
                          @error=${this._onImageError}
                          @load=${this._onImageLoad}
                        />
                      `:r`<ha-svg-icon .path=${a} slot="item-icon"></ha-svg-icon>`}
                  <paper-item-body
                    @click=${()=>this._showReopsitoryInfo(String(o.id))}
                    three-line
                    >${o.name}
                    <div secondary>${o.description}</div>
                    <div secondary>Category: ${o.category}</div></paper-item-body
                  >
                  <mwc-icon-button @click=${()=>this._removeRepository(o.id)}>
                    <ha-svg-icon class="delete" .path=${s}></ha-svg-icon>
                  </mwc-icon-button>
                </paper-icon-item>`)}
          </div>
        </div>
        <div class="add-repository" ?narrow=${this.narrow}>
          <input
            id="add-input"
            class="add-input"
            slot="secondaryaction"
            placeholder="${this.hacs.localize("dialog_custom_repositories.url_placeholder")}"
            .value=${this._inputRepository||""}
            @input=${this._inputValueChanged}
            ?narrow=${this.narrow}
          />

          <ha-paper-dropdown-menu
            ?narrow=${this.narrow}
            class="category"
            label="${this.hacs.localize("dialog_custom_repositories.category")}"
          >
            <paper-listbox id="category" slot="dropdown-content" selected="-1">
              ${this.hacs.configuration.categories.map(o=>r`
                  <paper-item class="categoryitem" .category=${o}>
                    ${this.hacs.localize("common."+o)}
                  </paper-item>
                `)}
            </paper-listbox>
          </ha-paper-dropdown-menu>
          <mwc-button
            ?narrow=${this.narrow}
            slot="primaryaction"
            raised
            @click=${this._addRepository}
          >
            ${this.hacs.localize("common.add")}
          </mwc-button>
        </div>
      </hacs-dialog>
    `}},{kind:"method",key:"firstUpdated",value:function(){this.hass.connection.subscribeEvents(o=>this._error=o.data,"hacs/error")}},{kind:"method",key:"_inputValueChanged",value:function(){var o;this._inputRepository=null===(o=this._addInput)||void 0===o?void 0:o.value}},{kind:"method",key:"_addRepository",value:async function(){var o,t;this._error=void 0;const i=this._inputRepository,e=null===(o=this._addCategory)||void 0===o||null===(t=o.selectedItem)||void 0===t?void 0:t.category;e?i?(await n(this.hass,i,e),this.repositories=await d(this.hass)):this._error={message:this.hacs.localize("dialog_custom_repositories.no_repository")}:this._error={message:this.hacs.localize("dialog_custom_repositories.no_category")}}},{kind:"method",key:"_removeRepository",value:async function(o){this._error=void 0,await c(this.hass,o),this.repositories=await d(this.hass)}},{kind:"method",key:"_onImageLoad",value:function(o){o.target.style.visibility="initial"}},{kind:"method",key:"_onImageError",value:function(o){o.target&&(o.target.outerHTML=`<ha-svg-icon path="${a}" slot="item-icon"></ha-svg-icon>`)}},{kind:"method",key:"_showReopsitoryInfo",value:async function(o){this.dispatchEvent(new CustomEvent("hacs-dialog-secondary",{detail:{type:"repository-info",repository:o},bubbles:!0,composed:!0}))}},{kind:"get",static:!0,key:"styles",value:function(){return[l,p,h`
        .content {
          width: 1024px;
          display: contents;
        }
        .list {
          position: relative;
          margin-top: 16px;
          max-height: 870px;
          overflow: auto;
        }
        ha-svg-icon {
          --mdc-icon-size: 36px;
        }
        img {
          align-items: center;
          display: block;
          justify-content: center;
          margin-bottom: 16px;
          max-height: 36px;
          max-width: 36px;
          position: absolute;
        }
        .delete {
          color: var(--hacs-error-color, var(--google-red-500));
        }
        paper-item-body {
          cursor: pointer;
        }

        paper-item-body {
          width: 100%;
          min-height: var(--paper-item-body-two-line-min-height, 72px);
          display: var(--layout-vertical_-_display);
          flex-direction: var(--layout-vertical_-_flex-direction);
          justify-content: var(--layout-center-justified_-_justify-content);
        }
        paper-item-body div {
          font-size: 14px;
          color: var(--secondary-text-color);
        }
        .add-repository {
          display: grid;
          width: 100%;
          justify-items: right;
        }

        .add-input {
          width: 100%;
          height: 40px;
          margin-top: 32px;
          border: 0;
          border-bottom: 1px var(--mdc-theme-primary) solid;
          text-align: left;
          padding: 0px;
          font-size: initial;
          color: var(--sidebar-text-color);
          font-family: var(--paper-font-body1_-_font-family);
        }
        input:focus {
          outline-offset: 0;
          outline: 0;
        }
        input {
          background-color: var(--sidebar-background-color);
        }
        ha-paper-dropdown-menu {
          width: 100%;
        }
        mwc-button {
          width: fit-content;
          margin-top: 16px;
        }

        input[narrow],
        .add-repository[narrow],
        ha-paper-dropdown-menu[narrow],
        mwc-button[narrow] {
          margin: 0;
          padding: 0;
          left: 0;
          top: 0;
          width: 100%;
          max-width: 100%;
        }
        .add-repository[narrow] {
          display: contents;
        }
      `]}}]}}),t);export{v as HacsCustomRepositoriesDialog};
