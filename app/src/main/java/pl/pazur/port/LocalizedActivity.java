package pl.pazur.port;

/** Share the selected locale without changing the phone's system language. */
public abstract class LocalizedActivity extends android.app.Activity {
    @Override protected void attachBaseContext(android.content.Context context) {
        super.attachBaseContext(AppLanguage.wrap(context));
    }
}
