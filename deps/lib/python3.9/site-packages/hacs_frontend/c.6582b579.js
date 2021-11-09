import{_ as o,H as i,e as t,o as e,T as r,c as a,K as s,N as n,O as d,Q as c,d as l,r as p,n as h}from"./main-60575625.js";import"./c.b82b3683.js";import"./c.5bd359ff.js";import"./c.75898fa6.js";import"./c.a1ea1e73.js";import"./c.0f3aa98b.js";import"./c.40bbc652.js";import"./c.5325c693.js";import"./c.386ba692.js";import"./c.d3dbc78b.js";let u=o([h("hacs-custom-repositories-dialog")],(function(o,i){return{F:class extends i{constructor(...i){super(...i),o(this)}},d:[{kind:"field",decorators:[t()],key:"_inputRepository",value:void 0},{kind:"field",decorators:[t()],key:"_error",value:void 0},{kind:"field",decorators:[e("#add-input")],key:"_addInput",value:void 0},{kind:"field",decorators:[e("#category")],key:"_addCategory",value:void 0},{kind:"method",key:"shouldUpdate",value:function(o){return o.has("narrow")||o.has("active")||o.has("_error")||o.has("repositories")}},{kind:"method",key:"render",value:function(){var o;if(!this.active)return r``;const i=null===(o=this.repositories)||void 0===o?void 0:o.filter(o=>o.custom);return r`
      <hacs-dialog
        .active=${this.active}
        .hass=${this.hass}
        .title=${this.hacs.localize("dialog_custom_repositories.title")}
        hideActions
      >
        <div class="content">
          <div class="list">
            ${this._error?r`<div class="error">${this._error.message}</div>`:""}
            ${null==i?void 0:i.filter(o=>this.hacs.configuration.categories.includes(o.category)).map(o=>r`<paper-icon-item>
                  ${"integration"===o.category?r`
                        <img
                          loading="lazy"
                          src="https://brands.home-assistant.io/_/${o.domain}/icon.png"
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
    `}},{kind:"method",key:"firstUpdated",value:function(){this.hass.connection.subscribeEvents(o=>this._error=o.data,"hacs/error")}},{kind:"method",key:"_inputValueChanged",value:function(){var o;this._inputRepository=null===(o=this._addInput)||void 0===o?void 0:o.value}},{kind:"method",key:"_addRepository",value:async function(){var o,i;this._error=void 0;const t=this._inputRepository,e=null===(o=this._addCategory)||void 0===o||null===(i=o.selectedItem)||void 0===i?void 0:i.category;e?t?(await n(this.hass,t,e),this.repositories=await d(this.hass)):this._error={message:this.hacs.localize("dialog_custom_repositories.no_repository")}:this._error={message:this.hacs.localize("dialog_custom_repositories.no_category")}}},{kind:"method",key:"_removeRepository",value:async function(o){this._error=void 0,await c(this.hass,o),this.repositories=await d(this.hass)}},{kind:"method",key:"_onImageLoad",value:function(o){o.target.style.visibility="initial"}},{kind:"method",key:"_onImageError",value:function(o){o.target.outerHTML='<ha-icon\n      icon="mdi:github-circle"\n      slot="item-icon"\n    ></ha-icon>'}},{kind:"method",key:"_showReopsitoryInfo",value:async function(o){this.dispatchEvent(new CustomEvent("hacs-dialog-secondary",{detail:{type:"repository-info",repository:o},bubbles:!0,composed:!0}))}},{kind:"get",static:!0,key:"styles",value:function(){return[l,p`
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
        ha-icon {
          color: var(--secondary-text-color);
        }
        ha-icon {
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
        .error {
          line-height: 0px;
          margin: 12px;
          color: var(--hacs-error-color, var(--google-red-500, red));
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
      `]}}]}}),i);export{u as HacsCustomRepositoriesDialog};
