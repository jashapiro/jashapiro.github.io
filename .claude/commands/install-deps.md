Install R package dependencies and any required system libraries for this project.

First, ensure system libraries are present (needed for source builds of packages like ragg, systemfonts, curl, xml2):

```bash
sudo apt-get install -y libfontconfig1-dev libfreetype-dev libharfbuzz-dev \
  libfribidi-dev libcurl4-openssl-dev libssl-dev libxml2-dev \
  libpng-dev libtiff-dev libjpeg-dev
```

Then restore the renv package library from the lockfile:

```bash
Rscript -e "renv::restore()"
```

If renv itself is not bootstrapped yet (no `renv/library/` for the current platform), the `.Rprofile` will auto-bootstrap it on first `Rscript` invocation — just re-run the restore command if it exits early the first time.
