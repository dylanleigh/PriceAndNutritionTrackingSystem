/*
* This is a connector for javascript to the PANTS api.
*/

/**
 * Encompassing class for the API, manages connecting to the remote resource and ferrying results back
 */
class Pants {
    /**
     *
     * @param {string} api_version The version of the api to use
     * @param {Object} authentication Describes what authentication method you are using
     * @param {string} authentication.method either "Basic", or "Token"
     * @param {string} authentication.token CSRF token to use for requests
     * @param {string} authentication.username  username to use for basic auth requests
     * @param {string} authentication.password  password to use for basic auth requests
     * @param {string} api_hostname The hostname of the server, if not passed in it will use window.location.host (which includes the port)
     */
    constructor(api_version, authentication, api_hostname) {
        this.api_location = `http://${api_hostname || window.location.host}/api/${api_version}/`;
        this.authentication_method = authentication.method;
        if(authentication.method === "Basic"){
            this.api_uname = authentication.username;
            this.api_pword = authentication.password;
        }
        else{
            this.token = authentication.token;
        }
    }

    /**
     * Gets a fully qualified path to a specific api resource, given a relative path
     * @param relative_path The relative api path to access, e.g. 'ingredient/280'
     */
    get_api_path(relative_path){
        return this.api_location + relative_path
    }

    get_basic_auth_credentials() {
        return 'Basic ' + btoa(`${this.api_uname}:${this.api_pword}`)
    }

    /**
     * Fetch, but with authentication automatically handled according to what authentication this API was instantiated with
     * @param url
     * @param init
     * @returns {Promise<Response>}
     */
    async authenticated_fetch(url, init) {
        // Ensure the Headers object is present
        init = init || {};

        if (init.headers === undefined) {
            init.headers = new Headers()
        }
        if(!(init.headers instanceof Headers)){
            // It is valid to just pass in an object, but we only deal with Headers. Convert
            var headers = new Headers();
            Object.entries(init.headers).forEach(entry=>{
                headers.set(entry[0], entry[1]);
            })
            init.headers = headers;
        }

        if (this.authentication_method === "Basic") {
            init.headers.set("Authorization", this.get_basic_auth_credentials());
        } else {
            init.headers.set("X-CSRFToken", this.token);
        }

        return fetch(url, init)
            .then(this.handle_api_errors)
            .catch(reason => alert(reason))
    }

    /**
     * Gets a list of ingredients, supports searching, limit, offset, ordering
     *
     * @param {Object} options Options to pass to the api
     * @param {number} options.limit Maximum number of results to return
     * @param {number} options.offset Which ingredient to start returning results from
     * @param {string} options.ordering 
     *
     * @returns {Promise<void>}
     */
    async get_ingredients(options) {

        // Get the number of requested results
        let num_requested = options.endRow - options.startRow;

        let api_location = new URL(this.get_api_path('ingredient/'));
        api_location.searchParams.set('offset', options.startRow);
        api_location.searchParams.set('limit', num_requested);

        // Handle sorting options
        let ordering = [];
        for (let id of options.sortModel) {
            let param = '';
            param += id.sort === 'desc' ? '-' : '';
            param += id.colId;
            ordering.push(param)
        }
        api_location.searchParams.set('ordering', ordering.join(','));

        // Handle searching options
        api_location.searchParams.set('search', document.querySelector('#ingredient_filter').value);

        // Fetch the data
        return this.authenticated_fetch(api_location.toString());
    }

    /**
     * Reusable function for handling errors from the api
     */
    async handle_api_errors(response) {
        if (!response.ok) {
            throw Error(await response.text())
        }
        return response
    }

    /**
     * Updates an ingredient (identified by uri) based on the json object passed in
     * @param uri {string} The URI that uniquely identifies the given ingredient
     * @param json_details {Object} The details that will be overwritten onto the ingredient (details not included are unaffected)
     */
    async edit_ingredient(uri, json_details) {
        return this.authenticated_fetch(uri, {
            method: 'PATCH',
            headers: new Headers({
                'Content-Type': 'application/json'
            }),
            body: JSON.stringify(json_details)
        })
            .then(resp => resp.json())
    }

    /**
     * Deletes the currently selected ingredient
     * @param ingredient_uri {string} The ingredient to delete
     */
    async delete_ingredient(ingredient_uri){
        // Send the command to delete the ingredient using the api
        return this.authenticated_fetch(ingredient_uri, {
            method: 'DELETE',
        })
    }

    /**
     * Creates a new ingredient using the information in the input fields
     * @param json_details {Object} The information for the ingredient
     */
    async create_ingredient(json_details){
        return this.authenticated_fetch(this.get_api_path('ingredient/'), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(json_details)
        })
            .then(resp => resp.json())
    }


}

